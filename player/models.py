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

from music.models import Music, PlaylistTrack


def generate_token():
    return binascii.b2a_hex(os.urandom(32))


class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    current_music = models.ForeignKey('music.Music', null=True, related_name="+", editable=False, on_delete=models.PROTECT)
    shuffle = models.BooleanField(default=False)
    can_adjust_volume = models.BooleanField(default=False)
    token = models.CharField(max_length=64, default=generate_token)
    tracks = models.ManyToManyField('music.Music', through='music.PlaylistTrack', related_name="+")

    def __str__(self):
        return self.name

    def reset_token(self):
        self.token = generate_token()
        self.save()

    def send_message(self, message):
        redis_publisher = RedisPublisher(facility=self.token, broadcast=True)
        message = RedisMessage(json.dumps(message))
        redis_publisher.publish_message(message)

    def play(self, music=None):
        # clear the queue
        if events[self.name]:
            events[self.name].cancel()

        if music:
            self.current_music = music
            self.save()
            if not music.is_valid():
                self.signal_dead_link()
                self.play_next()
            else:
                music.count += 1
                music.last_play = datetime.now()
                music.save()

                message = {
                    'action': 'play',
                    'update': True,
                    'source': music.source,
                    'options': {
                        'name': music.name,
                        'musicId': music.music_id,
                        'timer_start': music.timer_start,
                    }
                }
                if music.timer_end:
                    message['options']['timer_end'] = music.timer_end

                self.send_message(message)
                events[self.name] = Timer(music.duration, self.play_next, ())
                events[self.name].start()
        else:
            self.current_music = None
            self.save()
            message = {
                'stop': True,
                'update': True,
            }
            self.send_message(message)

    def play_next(self, forced=False):
        next_music = None
        previous_music = self.current_music
        if previous_music:
            if forced:
                next_music = previous_music
            else:
                next_music = self.tracks.all().order_by('playlisttrack__order').first()

        if next_music:
            PlaylistTrack.objects.filter(room=self, track=next_music).delete()
            self.play(music=next_music)

        elif self.shuffle:
            # Select random music, excluding 10% last played musics
            musics = self.music_set.exclude(dead_link=True).order_by('-date')
            count = musics.count()

            to_remove = int(count / 10)
            count -= to_remove
            musics = musics[to_remove:]
            a = count / float(5)  # Le point où ca commence à monter
            b = count / float(27)  # La vitesse à laquelle ca monte
            x = random.uniform(1, count - a - 1)
            i = int(math.floor(x + a - a * math.exp(-x / b)))

            shuffled = musics[i]
            shuffled.date = datetime.now()
            shuffled.save()

            self.play(music=shuffled)
        else:
            self.play(music=None)

    def push(self, music_id, requestId=None, **kwargs):
        music = Music.add(
            room=self,
            music_id=music_id,
            name=kwargs['name'],
            duration=kwargs['duration'],
            thumbnail=kwargs['thumbnail'],
            url=kwargs['url'],
            timer_start=kwargs['timer_start'],
            timer_end=kwargs['timer_end'],
            source=kwargs['source']
        )

        # Autoplay
        if not self.current_music:
            self.current_music = music
            self.save()
            self.play_next(forced=True)
        else:
            self.send_update_message()

    def get_current_remaining_time(self):
        if self.current_music:
            time = self.current_music.duration - int((datetime.now() - self.current_music.last_play).total_seconds())
            return int(time)
        return 0

    def get_remaining_time(self):
        if self.current_music:
            time_left = self.tracks.all().aggregate(Sum('duration')).get("sum__duration") or 0
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
            current_total_time = self.current_music.duration
            current_time_left = self.get_current_remaining_time()
            current_time_past_percent = ((current_total_time - current_time_left) * 100) / current_total_time
            return current_time_past_percent
        return 0

    def get_musics_remaining(self):
        if self.current_music:
            return self.tracks.all().order_by('playlisttrack__order')
        return []

    def get_count_remaining(self):
        if self.current_music:
            return self.tracks.count()
        return 0

    def signal_dead_link(self):
        if self.current_music:
            self.current_music.dead_link = True
            self.current_music.save()

    def increase_volume(self):
        if self.can_adjust_volume:
            message = {
                'action': 'volume_up',
                'source': self.current_music.source,
            }
            self.send_message(message)

    def decrease_volume(self):
        if self.can_adjust_volume:
            message = {
                'action': 'volume_down',
                'source': self.current_music.source,
            }
            self.send_message(message)

    def toggle_shuffle(self, to_active):
        if to_active:
            self.shuffle = True
            self.save()
            if not self.current_music:
                self.play_next()
            else:
                self.send_update_message()
        else:
            self.shuffle = False
            self.save()
            self.send_update_message()

    def order_playlist(self, pk, action, target=None):
        if action not in ['top', 'up', 'down', 'bottom', 'to']:
            return
        playlist = PlaylistTrack.objects.get(room=self, track__pk=pk)
        if target or target == 0:
            getattr(playlist, action)(target)
        else:
            getattr(playlist, action)()
        self.send_update_message()

    def send_update_message(self):
        message = {
                'update': True,
        }
        self.send_message(message)

events = dict()


from player.signals import *
