from django.db import models

import webbrowser
import psutil


class Category (models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Url(models.Model):
    url = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    played = models.BooleanField(default=False)

    def __unicode__(self):
        return self.url


class Play(models.Model):
    actual = models.ForeignKey(Url, default=None)

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
            return
        url = Url.objects.filter(date__lt=self.actual.date).first()
        if not url:
            return

        self.actual = url
        self.save()

        PROCNAME = 'firefox.exe'
        for process in psutil.process_iter():
            if process.name == PROCNAME:
                process.kill()

        webbrowser.open(url.url)

    def reset(self):
        self.actual = Url.objects.filter(date__lt=self.actual.date).last()
        self.save()
