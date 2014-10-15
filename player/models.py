# -*- coding: utf-8 -*-

from django.db import models

import webbrowser
from datetime import datetime
from threading import Timer
from player.helpers import youtube


class Music(models.Model):
    # Youtube ID
    video_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, editable=False)
    # Date is used for ordering musics
    date = models.DateTimeField(auto_now_add=True)
    # Duration in second
    duration = models.PositiveIntegerField(editable=False)
    # thumbnail in 190 * 120
    thumbnail = models.CharField(max_length=255, editable=False)
    count = models.PositiveIntegerField(default=0, editable=False)
    last_play = models.DateTimeField(null=True)
    # signalement de lien mort
    lien_mort = models.BooleanField(default=True)

    @classmethod
    def add(cls, **kwargs):
        existing_music = Music.objects.filter(video_id=kwargs['video_id']).first()
        if existing_music:
            existing_music.date = datetime.now()
            existing_music.save()
            return existing_music
        else:
            music = cls(**kwargs)
            music.save()
            return music

    @classmethod
    def search(self, string):
        list_music = Music.objects.filter(name__icontains=string)
        return list_music

    def __unicode__(self):
        return self.name


class Player():
    current = None
    event = None
    shuffle = False

    STOP_URL = "https://www.google.fr"

    @classmethod
    def play(self, music=None):
        # clear the queue
        if Player.event:
            Player.event.cancel()

        if music:
            Player.current = music
            music.count += 1
            music.last_play = datetime.now()
            music.save()

            webbrowser.open(youtube.get_link(music.video_id))

            Player.event = Timer(music.duration, Player.play_next, ())
            Player.event.start()
        else:
            webbrowser.open(Player.STOP_URL)

    @classmethod
    def play_next(self, forced=False):
        music = None
        if Player.current:
            if forced:
                music = Player.current
            else:
                music = Music.objects.filter(date__gt=Player.current.date).order_by('date').first()

        if music:
            Player.play(music)
        elif Player.shuffle:
            # Select random music, excluding 5% last played musics
            count = Music.objects.all().count()
            limit = count / 20
            limit_date = Music.objects.all().order_by('-date')[limit].date
            shuffled = Music.objects.filter(date__lte=limit_date).exclude(lien_mort=False).order_by('?').first()
            shuffled.date = datetime.now()
            shuffled.save()

            Player.play(shuffled)
        else:
            Player.current = None
            Player.play(None)

    @classmethod
    def push(self, video_id):
        music = Music.add(video_id=video_id)

        if not Player.current:
            Player.current = music
            Player.play_next(forced=True)

    @classmethod
    def get_current_remaining_time(self):
        if not Player.current:
            return 0
        time = Player.current.duration - int(((datetime.now() - Player.current.last_play)).total_seconds())
        return int(time)

    @classmethod
    def get_remaining_time(self):
        if not Player.current:
            return 0
        nexts = Music.objects.filter(date__gt=Player.current.date)
        time_left = 0
        for music in nexts:
            time_left += music.duration
        time_left += Player.get_current_remaining_time()
        return int(time_left)

    @classmethod
    def get_musics_remaining(self):
        if not Player.current:
            return
        nexts = Music.objects.filter(date__gt=Player.current.date).order_by('date')

        return nexts

    @classmethod
    def get_count_remaining(self):
        if not Player.current:
            return 0
        return Music.objects.filter(date__gte=Player.current.date).count()

    @classmethod
    def signal_lien_mort(self):
        if not Player.current:
            return
        Player.current.lien_mort = True
        Player.current.save()

from player.signals import *
