from django.db import models
from django.db.models import Sum

import random
import math
import os
import binascii
import json
from datetime import datetime
from threading import Timer
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from django.conf import settings

from music.models import PlaylistTrack


def generate_token():
    return str(binascii.b2a_hex(os.urandom(32)))


class UnableToUpdate(Exception):
    """
    Error triggered when room's update is impossible
    """
    pass


class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    current_music = models.ForeignKey('music.Music', null=True, related_name="+", editable=False, on_delete=models.PROTECT)
    shuffle = models.BooleanField(default=False)
    can_adjust_volume = models.BooleanField(default=False)
    token = models.CharField(max_length=64, default=generate_token)
    tracks = models.ManyToManyField('music.Music', through='music.PlaylistTrack', related_name="+")
    volume = models.PositiveIntegerField(default=10)
    listeners = models.PositiveIntegerField(editable=False, default=0)

    UnableToUpdate = UnableToUpdate

    setters = {
        'with_setters': ['shuffle', 'volume'],
        'without_setters': ['can_adjust_volume'],
    }

    def __str__(self):
        return "{} \n playing: {}".format(self.name, self.current_music)

    def update(self, modifications):
        for key, value in modifications.items():
            if key in Room.setters['with_setters']:
                getattr(self, 'set_%s' % key)(value)
            elif key in Room.setters['without_setters']:
                setattr(self, key, value)
                self.save()

    def reset_token(self):
        self.token = generate_token()
        self.save()

    def send_message(self, message):
        redis_publisher = RedisPublisher(facility=self.token, broadcast=True)
        message = RedisMessage(json.dumps(message))
        listeners = redis_publisher.publish_message(message)[settings.WS4REDIS_PREFIX + ":broadcast:" + self.token]
        if listeners != self.listeners:
            self.listeners = listeners
            self.save()
            message = {
                'action': 'listeners_updated',
                'listeners': self.listeners
            }
            listenersMessage = RedisMessage(json.dumps(message))
            redis_publisher.publish_message(listenersMessage)

    def play(self, music):
        # clear the queue
        event = Events.get(self)
        if event:
            event.cancel()

        self.current_music = music
        self.save()
        if not music.is_valid():
            self.play_next()
            music.delete()
        else:
            music.count += 1
            music.last_play = datetime.now()
            music.save()

            message = {
                'action': 'play',
                'room': self.get_serialized_room(),
            }

            self.send_message(message)

            # Tricky code that create a new thread. Be careful about asynchronousity
            event = Events.set(self, Timer(music.duration, self.play_next, ()))
            event.start()

    def stop(self):
        self.current_music = None
        self.save()
        message = {
            'action': 'stop',
        }
        self.send_message(message)

    def play_next(self):
        self.refresh_from_db()
        next_music = self.tracks.all().order_by('playlisttrack__order').first()

        if next_music:
            PlaylistTrack.objects.filter(room=self, track=next_music).first().delete()
            self.play(music=next_music)

        elif self.shuffle:
            shuffled = self.select_random_music()
            shuffled.date = datetime.now()
            shuffled.save()

            self.play(music=shuffled)
        else:
            self.stop()

    def add_music(self, music):
        # Adding the music to the queue
        PlaylistTrack.objects.create(room=self, track=music)

        # Autoplay
        if not self.current_music:
            self.play_next()
        else:
            message = {
                'action': 'music_added',
                'playlistTracks': self.get_serialized_playlist(),
            }
            self.send_message(message)

    def select_random_music(self):
        # Select random music, excluding 10% last played musics
        musics = self.music_set.exclude(duration__gte=600).order_by('-last_play')
        count = musics.count()

        to_remove = int(count / 10)
        count -= to_remove
        musics = musics[to_remove:]

        a = count / float(5)  # Le point où ca commence à monter
        b = count / float(27)  # La vitesse à laquelle ca monte
        x = random.uniform(1, count - a - 1)
        i = min(int(math.floor(x + a - a * math.exp(-x / b))), len(musics) - 1)  # Can't select out of range music
        if i < 0:
            i = 0  # Can't get negative index

        return musics[i]

    def get_current_remaining_time(self):
        if self.current_music:
            time = self.current_music.duration - int((datetime.now() - self.current_music.last_play).total_seconds())
            return int(time)
        return 0

    def get_remaining_time(self):
        if self.tracks.count() > 0:
            time_left = self.tracks.all().aggregate(Sum('duration')).get("duration__sum") or 0
            time_left += self.get_current_remaining_time()
            return int(time_left)
        return 0

    def get_current_time_past(self):
        if self.current_music:
            current_time_past = self.current_music.duration - self.get_current_remaining_time()
            return current_time_past
        return 0

    def get_current_time_past_percent(self):
        if self.current_music:
            try:
                current_total_time = self.current_music.duration
                current_time_left = self.get_current_remaining_time()
                current_time_past_percent = ((current_total_time - current_time_left) * 100) / current_total_time
                return current_time_past_percent
            except ZeroDivisionError:
                pass
        return 0

    def get_musics_remaining(self):
        return self.tracks.all().order_by('playlisttrack__order')

    def get_count_remaining(self):
        return self.tracks.count()

    def set_volume(self, volume):
        if not self.can_adjust_volume:
            raise UnableToUpdate("This room don't have permission to update volume.")

        self.volume = volume
        self.save()

        message = {
            'action': 'volume_changed',
            'volume': self.volume
        }
        self.send_message(message)

    def set_shuffle(self, to_active):
        if to_active and self.music_set.count() == 0:
            raise self.UnableToUpdate("Can't activate shuffle when there is no musics.")
        if to_active:
            self.shuffle = True
            message = {
                'action': 'shuffle_changed',
                'shuffle': True,
            }
            self.save()
            self.send_message(message)
            if not self.current_music:
                self.play_next()
        else:
            self.shuffle = False
            message = {
                'action': 'shuffle_changed',
                'shuffle': False,
            }
            self.save()
            self.send_message(message)

    def get_serialized_playlist(self):
        # Horrible but Mom said me I can :3
        # http://sametmax.com/quelques-erreurs-tordues-et-leurs-solutions-en-python/
        from music.serializers import PlaylistSerializer
        return PlaylistSerializer(self.playlist.all(), many=True).data

    def get_serialized_room(self):
        # Horrible but Mom said me I can :3
        # http://sametmax.com/quelques-erreurs-tordues-et-leurs-solutions-en-python/
        from player.serializers import RoomSerializer
        return RoomSerializer(self).data


class Events():
    events = dict()

    @classmethod
    def get(cls, room):
        return cls.events[room.name]

    @classmethod
    def set(cls, room, value=None):
        cls.events[room.name] = value
        return value

    @classmethod
    def get_all(cls):
        return cls.events


from player.signals import *
