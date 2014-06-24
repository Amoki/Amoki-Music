from django.db import models

import webbrowser
import psutil


class Category (models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Url(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    played = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def replay(self):
        Url(url=self.url, category=self.category).save()


class Play(models.Model):
    actual = models.ForeignKey(Url, null=True, editable=False)

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
            return

        self.actual = url
        self.save()

        PROCNAME = u'firefox.exe'
        for process in psutil.process_iter():
            print process.name
            if process.name == PROCNAME:
                print ("killing %s", PROCNAME)
                process.kill()

        webbrowser.open(url.url)

    def reset(self):
        self.actual = Url.objects.filter(date__lt=self.actual.date).last()
        self.save()


from browser.signals import *
