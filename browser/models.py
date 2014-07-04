from django.db import models

import webbrowser
from datetime import datetime
from threading import Timer
from browser.helpers import get_youtube_link


class Category (models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Music(models.Model):
    video_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    playing_date = models.DateTimeField(null=True)
    category = models.ForeignKey(Category)
    duration = models.PositiveIntegerField(editable=False)

    @classmethod
    def get_unique(self):
        checked_musics = []
        musics = []
        for music in Music.objects.all():
            if [music.video_id, music.category] not in checked_musics:
                musics.append(music)
                checked_musics.append([music.video_id, music.category])
        return musics

    def get_played_count(self):
        return Music.objects.filter(video_id=self.video_id).count()

    def __unicode__(self):
        return self.name


class Player(models.Model):
    actual = models.ForeignKey(Music, null=True, editable=False)
    event = None

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(Player, self).save(*args, **kwargs)

    @classmethod
    def load(self):
        try:
            return Player.objects.get()
        except Player.DoesNotExist:
            player = Player()
            player.save()
            return player

    def play_next(self, forced=False):
        # clear the queue
        if Player.event:
            Player.event.cancel()

        music = None

        if self.actual:
            if not forced:
                music = Music.objects.filter(date__gt=self.actual.date).first()
            else:
                music = self.actual

        if not music:
            self.actual = None
            self.save()
        else:
            self.actual = music
            self.save()
            music.playing_date = datetime.now()
            music.save()

            webbrowser.open(get_youtube_link(music.video_id))

            Player.event = Timer(music.duration, self.play_next, ())
            Player.event.start()

    def push(self, video_id, category):
        music = Music(video_id=video_id, category=category)
        music.save()

        if not self.actual:
            self.actual = music
            self.save()
            self.play_next(forced=True)

    def get_actual_remaining_time(self):
        if not self.actual:
            return 0
        return self.actual.duration - int(((datetime.now() - self.actual.playing_date)).total_seconds())

    def get_remaining_time(self):
        if not self.actual:
            return 0
        nexts = Music.objects.filter(date__gt=self.actual.date)
        time_left = 0
        for music in nexts:
            time_left += music.duration
        time_left += self.get_actual_remaining_time()

        return time_left

    def get_musics_remaining(self):
        if not self.actual:
            return
        nexts = Music.objects.filter(date__gt=self.actual.date)

        return map(str, nexts)

    def get_number_remaining(self):
        if not self.actual:
            return 0
        return Music.objects.filter(date__gte=self.actual.date).count()


from browser.signals import *
