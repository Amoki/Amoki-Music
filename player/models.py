# -*- coding: utf-8 -*-

from django.db import models
import django_socketio
import urlparse
from datetime import datetime, timedelta
from threading import Timer


class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    current_music = models.ForeignKey('player.Music', null=True, related_name="+", editable=False)
    shuffle = models.BooleanField(default=False)

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

            message = dict()
            message['action'] = "play"
            message['name'] = music.name

            url_data = urlparse.urlparse(music.url)
            video_id = urlparse.parse_qs(url_data.query)["v"][0]

            message['video_id'] = video_id
            try:
                django_socketio.broadcast_channel(message, self.name)
                events[self.name] = Timer(music.duration, self.play_next, ())
                events[self.name].start()
            except:
                pass
        else:
            message = dict()
            message['action'] = "stop"
            try:
                django_socketio.broadcast_channel(message, self.name)
            except:
                pass

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
            # Select random music, excluding 5% last played musics
            count = self.music_set.all().count()
            limit = count / 20
            limit_date = self.music_set.all().order_by('-date')[limit].date
            shuffled = self.music_set.filter(date__lte=limit_date).exclude(dead_link=True).order_by('?').first()
            shuffled.date = datetime.now()
            shuffled.save()

            self.play(shuffled)
        else:
            self.current_music = None
            self.save()
            self.play(None)

    def push(self, url, requestId=None):
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
            # TODO: get all video data
            music = Music.add(url=url, room=self)

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


class Music(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255, editable=False)
    room = models.ForeignKey(Room)
    # Date is used for ordering musics
    date = models.DateTimeField(auto_now_add=True)
    # Duration in second
    duration = models.PositiveIntegerField(editable=False)
    # thumbnail in 190 * 120
    thumbnail = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0, editable=False)
    last_play = models.DateTimeField(null=True)
    # signalement de lien mort
    dead_link = models.BooleanField(default=False)

    @classmethod
    def add(cls, **kwargs):
        existing_music = Music.objects.filter(url=kwargs['url']).first()
        if existing_music:
            existing_music.date = datetime.now()
            existing_music.save()
            return existing_music
        else:
            music = cls(**kwargs)
            music.save()
            return music

    def __unicode__(self):
        return self.name


class TemporaryMusic(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()
    thumbnail = models.CharField(max_length=255)
    views = models.PositiveIntegerField()
    description = models.TextField()
    requestId = models.CharField(max_length=64)

    @classmethod
    def clean(self):
        TemporaryMusic.objects.filter(date__lte=datetime.now() - timedelta(hours=1)).delete()


events = dict()


from player.signals import *
