from django.db import models
from datetime import datetime, timedelta


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
    timer_start = models.PositiveIntegerField(editable=False, default=0)
    timer_end = models.PositiveIntegerField(editable=False, null=True)

    @classmethod
    def add(cls, **kwargs):
        existing_music = Music.objects.filter(music_id=kwargs['music_id'], room=kwargs['room']).first()
        if existing_music:
            if existing_music.timer_end:
                duration = existing_music.duration - (existing_music.duration - existing_music.timer_end)
            duration = existing_music.duration - existing_music.timer_start
            if existing_music.duration != duration:
                existing_music.duration = duration
            existing_music.date = datetime.now()
            existing_music.save()
            return existing_music
        else:
            music = cls(**kwargs)
            if music.timer_end:
                music.duration = music.duration - (music.duration - music.timer_end)
            music.duration = music.duration - music.timer_start
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
