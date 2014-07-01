from django.db import models

import webbrowser
import psutil
import sched
import time


class Category (models.Model):
    name = models.CharField(max_length=255)

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
        return self.name

    def replay(self):
        Url(url=self.url, category=self.category).save()


class Play(models.Model):
    actual = models.ForeignKey(Url, null=True, editable=False)
    scheduler = sched.scheduler(time.time, time.sleep)

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(Play, self).save(*args, **kwargs)

    @classmethod
    def load():
        try:
            return Play.objects.get()
        except Play.DoesNotExist:
            play = Play()
            play.save()
            return play

    def play_next(self):
        if not self.actual:
            url = Url.objects.filter().first()
        else:
            url = Url.objects.filter(date__lt=self.actual.date).first()

        if not url:
            self.actual = None
            self.save()
            self.scheduler.enter(5, 1, play_next, (self,))
        else:
            self.actual = url
            self.save()
            url.played_count += 1
            url.save()

            PROCNAME = u'firefox.exe'
            for process in psutil.process_iter():
                try:
                    if process.name == PROCNAME:
                        print ("killing %s", PROCNAME)
                        process.kill()
                except:
                    pass

            webbrowser.open(url.url)

            self.scheduler.enter(url.duration, 1, play_next, (self,))

    def reset(self):
        self.actual = Url.objects.filter(date__lt=self.actual.date).last()
        self.save()


from browser.signals import *
