from django.db import models
from django.utils import timezone

import webbrowser
import psutil
from threading import Timer


class Category (models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Url(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    played_count = models.PositiveIntegerField(default=0, editable=False)
    duration = models.PositiveIntegerField(editable=False)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.played_count)

    def replay(self):
        Url(url=self.url, category=self.category).save()


class Player(models.Model):
    actual = models.ForeignKey(Url, null=True, editable=False)
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
        if self.event:
            self.event.cancel()

        url = None

        if self.actual:
            if not forced:
                url = Url.objects.filter(date__gt=self.actual.date).first()
            else:
                url = self.actual

        if not url:
            self.actual = None
            self.save()
        else:
            self.actual = url
            self.save()
            url.played_count += 1
            url.save()

            PROCNAME = u'firefox.exe'
            for process in psutil.process_iter():
                try:
                    if process.name == PROCNAME:
                        process.kill()
                except:
                    pass

            webbrowser.open(url.url)

            self.event = Timer(url.duration, self.play_next, ())
            self.event.start()

    def push(self, url, category):
        old_url = Url.objects.filter(url=url, category=category).first()
        if not old_url:
            old_url = Url(
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
        self.actual = Url.objects.filter(date__lt=self.actual.date).last()
        self.save()


from browser.signals import *
