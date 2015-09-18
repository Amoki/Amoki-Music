from django.db import models
from datetime import datetime

from ordered_model.models import OrderedModel
from sources import source


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
    source = models.CharField(max_length=255, editable=False)

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
            if existing_music.room.current_music != existing_music:
                try:
                    PlaylistTrack.objects.get(track=existing_music).top()
                except PlaylistTrack.DoesNotExist:
                    PlaylistTrack.objects.create(room=existing_music.room, track=existing_music)
            return existing_music
        else:
            music = cls(**kwargs)
            music.save()
            PlaylistTrack.objects.create(room=music.room, track=music)
            return music

    def __str__(self):
        return self.name

    def is_valid(self):
        return source.check_validity(self.source, self.music_id)


class PlaylistTrack(OrderedModel):
    room = models.ForeignKey('player.Room')
    track = models.ForeignKey('music.Music')
    order_with_respect_to = 'room'

    class Meta(OrderedModel.Meta):
        pass
