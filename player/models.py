# -*- coding: utf-8 -*-

from django.db import models

import django_socketio
import random
import math
import os
import binascii
from datetime import datetime
from threading import Timer

from music.models import Music, TemporaryMusic


def generate_token():
    return binascii.b2a_hex(os.urandom(32))


class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    current_music = models.ForeignKey('music.Music', null=True, related_name="+", editable=False)
    shuffle = models.BooleanField(default=False)
    can_adjust_volume = models.BooleanField(default=False)
    token = models.CharField(max_length=64, default=generate_token)

    def __unicode__(self):
        return self.name

    def reset_token(self):
        self.token = generate_token()
        self.save()

    def send_message(self, message):
        try:
            django_socketio.broadcast_channel(message, self.token)
            return True
        except:
            return False

    def play(self, music=None):
        # clear the queue
        if events[self.name]:
            events[self.name].cancel()

        if music:
            self.current_music = music
            self.save()
            music.count += 1
            music.last_play = datetime.now()
            music.save()

            message = {
                'action': 'play',
                'update': True,
                'options': {
                    'name': music.name,
                    'musicId': music.music_id,
                    'timer_start': music.timer_start,
                }
            }
            if music.timer_end:
                message['options']['timer_end'] = music.timer_end

            if self.send_message(message):
                events[self.name] = Timer(music.duration, self.play_next, ())
                events[self.name].start()
            else:
                self.shuffle = False
                self.current_music = None
                self.save()

        else:
            message = {
                'action': 'stop',
                'update': True,
            }
            self.send_message(message)

    def play_next(self, forced=False):
        music = None
        if self.current_music:
            if forced:
                music = self.current_music
            else:
                music = self.music_set.filter(date__gt=self.current_music.date).order_by('date').first()

        if music:
            self.play(music)
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

            self.play(shuffled)
        else:
            self.current_music = None
            self.save()
            self.play(None)

    def push(self, music_id, requestId=None, **kwargs):
        if requestId:
            temporaryMusic = TemporaryMusic.objects.get(music_id=music_id, requestId=requestId)
            music = Music.add(
                room=self,
                music_id=music_id,
                name=temporaryMusic.name,
                duration=temporaryMusic.duration,
                thumbnail=temporaryMusic.thumbnail,
                timer_start=kwargs['timer_start'],
                timer_end=kwargs['timer_end'],
            )
            TemporaryMusic.clean()
        else:
            music = Music.add(
                room=self,
                music_id=music_id,
                name=kwargs['name'],
                duration=kwargs['duration'],
                thumbnail=kwargs['thumbnail'],
                timer_start=kwargs['timer_start'],
                timer_end=kwargs['timer_end'],
            )

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
            nexts = self.music_set.filter(date__gt=self.current_music.date)
            time_left = 0
            for music in nexts:
                time_left += music.duration
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
            return self.music_set.filter(date__gt=self.current_music.date).order_by('date')
        return []

    def get_count_remaining(self):
        if self.current_music:
            return self.music_set.filter(date__gte=self.current_music.date).count()
        return 0

    def signal_dead_link(self):
        if self.current_music:
            self.current_music.dead_link = True
            self.current_music.save()

    def increase_volume(self):
        if self.can_adjust_volume:
            message = {
                'action': 'volume_up',
            }
            self.send_message(message)

    def decrease_volume(self):
        if self.can_adjust_volume:
            message = {
                'action': 'volume_down',
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

    def send_update_message(self):
        message = {
                'update': True,
        }
        self.send_message(message)

events = dict()


from player.signals import *
