from django.db import models
from django.utils import timezone

import webbrowser
import datetime
from threading import Timer


class Category (models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Music(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    played_count = models.PositiveIntegerField(default=0, editable=False)
    duration = models.PositiveIntegerField(editable=False)

    def __unicode__(self):
        return self.name

    def replay(self):
        Url(url=self.url, category=self.category).save()


event = None


def get_event():
    return event


def set_event(event):
    event = event


class Player(models.Model):
    actual = models.ForeignKey(Music, null=True, editable=False)

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
        if get_event():
            get_event().cancel()

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
            music.played_count += 1
            music.save()

            webbrowser.open(music.url, new=0)

            set_event(Timer(music.duration, self.play_next, ()))
            get_event().start()

    def push(self, url, category):
        old_url = Music.objects.filter(url=url, category=category).first()
        if not old_url:
            old_url = Music(
                url=url,
                category=category
            )
        else:
            old_url.date = timezone.now()
        old_url.save()

        if not self.actual:
            self.actual = old_url
            self.save()
            self.play_next(forced=True)

    def reset(self):
        self.actual = Music.objects.filter(date__gt=self.actual.date).last()
        self.save()

    def get_remaining_time(self):
        if not self.actual:
            return 0
        nexts = Music.objects.filter(date__gt=self.actual.date)
        time_left = 0
        for music in nexts:
            time_left += music.duration
        time_left = str(datetime.timedelta(seconds=time_left))
        return time_left

    def get_musics_remaining(self):
        if not self.actual:
            return
        nexts = Music.objects.filter(date__gt=self.actual.date)

        return map(str, nexts)

    def get_number_remaining(self):
        if not self.actual:
            return 0
        return Music.objects.filter(date__gt=self.actual.date).count()


from browser.signals import *
