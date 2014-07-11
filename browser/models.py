from django.db import models

import webbrowser
from datetime import datetime
from threading import Timer
from browser.helpers import get_youtube_link


class Music(models.Model):
    video_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    playing_date = models.DateTimeField(null=True)
    duration = models.PositiveIntegerField(editable=False)
    thumbnail = models.CharField(max_length=255, editable=False)

    @classmethod
    def get_unique(self):
        checked_musics = []
        musics = []
        for music in Music.objects.all().order_by('-date'):
            if music.video_id not in checked_musics:
                musics.append(music)
                checked_musics.append(music.video_id)
        return musics

    def get_played_count(self):
        return Music.objects.filter(video_id=self.video_id).count()

    def __unicode__(self):
        return self.name


class Player():
    actual = None
    event = None
    suffle = False

    @classmethod
    def play(music):
        # clear the queue
        if Player.event:
            Player.event.cancel()

        Player.actual = music
        music.playing_date = datetime.now()
        music.save()

        webbrowser.open(get_youtube_link(music.video_id))

        Player.event = Timer(music.duration, Player.play_next, ())
        Player.event.start()

    @classmethod
    def play_next(forced=False):
        music = None
        if Player.actual:
            if forced:
                music = Player.actual
            else:
                music = Music.objects.filter(date__gt=Player.actual.date).first()

        if not music and Player.suffle:
            music = Music.objects.filter().order_by('?').first()

        if music:
            Player.play(music)

    @classmethod
    def push(video_id):
        music = Music(video_id=video_id)
        music.save()

        if not Player.actual:
            Player.actual = music
            Player.play_next(forced=True)

    @classmethod
    def get_actual_remaining_time():
        if not Player.actual:
            return 0
        return Player.actual.duration - int(((datetime.now() - Player.actual.playing_date)).total_seconds())

    @classmethod
    def get_remaining_time():
        if not Player.actual:
            return 0
        nexts = Music.objects.filter(date__gt=Player.actual.date)
        time_left = 0
        for music in nexts:
            time_left += music.duration
        time_left += Player.get_actual_remaining_time()

        return time_left

    @classmethod
    def get_musics_remaining():
        if not Player.actual:
            return
        nexts = Music.objects.filter(date__gt=Player.actual.date)

        return map(str, nexts)

    @classmethod
    def get_number_remaining():
        if not Player.actual:
            return 0
        return Music.objects.filter(date__gte=Player.actual.date).count()


from browser.signals import *
