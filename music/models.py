from django.db import models
from datetime import datetime, timedelta


class Source(models.Model):
    name = models.CharField(max_length=255)
    regex = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def search(self, query=None, ids=None):
        Provider = None
        for cls in Source.__subclasses__():
            if cls.__name__ == self.name:
                Provider = cls

        return Provider.search(query=query, ids=ids)


class Music(models.Model):
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255, editable=False)
    room = models.ForeignKey('player.Room')
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
    timer_start = models.PositiveIntegerField(default=0)
    timer_end = models.PositiveIntegerField(null=True)
    source = models.ForeignKey(Source)

    @classmethod
    def add(cls, **kwargs):
        existing_music = Music.objects.filter(music_id=kwargs['music_id'], room=kwargs['room'], source=kwargs['source']).first()
        if existing_music:
            if kwargs['timer_start']:
                existing_music.timer_start = kwargs['timer_start']
            if kwargs['timer_end']:
                existing_music.timer_end = kwargs['timer_end']
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
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()
    thumbnail = models.CharField(max_length=255)
    views = models.PositiveIntegerField()
    description = models.TextField()
    requestId = models.CharField(max_length=64)

    @classmethod
    def clean(self):
        TemporaryMusic.objects.filter(date__lte=datetime.now() - timedelta(hours=1)).delete()
