# -*- coding: utf-8 -*-

from django.db import models

import django_socketio
import urlparse
import random
import math
import os
import binascii
from datetime import datetime
from threading import Timer

from music.models import Music


def generate_token():
    return binascii.b2a_hex(os.urandom(32))


class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    current_music = models.ForeignKey('music.Music', null=True, related_name="+", editable=False)
    shuffle = models.BooleanField(default=False)
    token = models.CharField(max_length=64, default=generate_token)

    def send_message(self, message, function=None):
        try:
            django_socketio.broadcast_channel(message, self.token)
            if function:
                function()
        except:
            pass

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

            url_data = urlparse.urlparse(music.url)
            video_id = urlparse.parse_qs(url_data.query)["v"][0]

            message = {
                'action': 'play',
                'options': {
                    'name': music.name,
                    'videoId': video_id
                }
            }

            def play_music():
                events[self.name] = Timer(music.duration, self.play_next, ())
                events[self.name].start()

            self.send_message(message, play_music)
        else:
            message = {
                'action': 'stop',
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
            musics = Music.objects.all().exclude(dead_link=True).order_by('-date')
            count = musics.count()

            to_remove = int(count / 10)
            count -= to_remove
            musics = musics[to_remove:]
            a = count / 5  # Le point où ca commence à monter
            b = count / 27  # La vitesse à laquelle ca monte
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

    def push(self, url, requestId=None, **kwargs):
        if requestId:
            temporaryMusic = TemporaryMusic.objects.get(url=url, requestId=requestId)
            music = Music.add(
                room=self,
                url=url,
                name=temporaryMusic.name,
                duration=temporaryMusic.duration,
                thumbnail=temporaryMusic.thumbnail
            )
            TemporaryMusic.clean()
        else:
            music = Music.add(
                room=self,
                url=url,
                name=kwargs['name'],
                duration=kwargs['duration'],
                thumbnail=kwargs['thumbnail']
            )

        if not self.current_music:
            self.current_music = music
            self.save()
            self.play_next(forced=True)

    def get_current_remaining_time(self):
        if not self.current_music:
            return 0
        time = self.current_music.duration - int(((datetime.now() - self.current_music.last_play)).total_seconds())
        return int(time)

    def get_remaining_time(self):
        if not self.current_music:
            return 0
        nexts = self.music_set.filter(date__gt=self.current_music.date)
        time_left = 0
        for music in nexts:
            time_left += music.duration
        time_left += self.get_current_remaining_time()
        return int(time_left)

    def get_musics_remaining(self):
        if not self.current_music:
            return
        return self.music_set.filter(date__gt=self.current_music.date).order_by('date')

    def get_count_remaining(self):
        if not self.current_music:
            return 0
        return self.music_set.filter(date__gte=self.current_music.date).count()

    def signal_dead_link(self):
        if not self.current_music:
            return
        self.current_music.dead_link = True
        self.current_music.save()

    def increase_volume(self):
        message = {
            'action': 'volume_up',
        }
        self.send_message(message)

    def decrease_volume(self):
        message = {
            'action': 'volume_down',
        }
        self.send_message(message)

events = dict()


from player.signals import *
