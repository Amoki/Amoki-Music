from django.db import models
from datetime import datetime, timedelta

from ordered_model.models import OrderedModel


class Source(models.Model):
    name = models.CharField(max_length=255, editable=False)

    def __unicode__(self):
        return self.name

    def search(self, query):
        Provider = None
        for cls in Source.__subclasses__():
            if cls.__name__ == self.name:
                Provider = cls

        return Provider.search(query)

    def check_validity(self, id):
        Provider = None
        for cls in Source.__subclasses__():
            if cls.__name__ == self.name:
                Provider = cls

        return Provider.check_validity(id)


class Music(models.Model):
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255, editable=False)
    url = models.CharField(max_length=512, editable=False)
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
    timer_end = models.PositiveIntegerField(null=True, blank=True)
    source = models.ForeignKey(Source, editable=False)

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
            if not existing_music.room.current_music == existing_music:
                if PlaylistTrack.objects.filter(track__pk=existing_music.pk):
                    PlaylistTrack.objects.get(track__pk=existing_music.pk).top()
                else:
                    PlaylistTrack.objects.create(room=existing_music.room, track=existing_music)

            return existing_music
        else:
            music = cls(**kwargs)
            music.save()
            PlaylistTrack.objects.create(room=music.room, track=music)
            return music

    def __unicode__(self):
        return self.name

    def is_valid(self):
        return self.source.check_validity(self.music_id)


class TemporaryMusic(models.Model):
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()
    thumbnail = models.CharField(max_length=255)
    views = models.PositiveIntegerField()
    description = models.TextField()
    url = models.CharField(max_length=512)
    requestId = models.CharField(max_length=64)
    source = models.ForeignKey(Source, editable=False)

    @classmethod
    def clean(self):
        TemporaryMusic.objects.filter(date__lte=datetime.now() - timedelta(hours=1)).delete()


class PlaylistTrack(OrderedModel):
    room = models.ForeignKey('player.Room')
    track = models.ForeignKey('music.Music')
    order_with_respect_to = 'room'

    class Meta(OrderedModel.Meta):
        pass
