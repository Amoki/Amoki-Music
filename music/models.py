from django.db import models

from ordered_model.models import OrderedModel
from sources import source


class Music(models.Model):
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255, editable=False)
    url = models.CharField(max_length=512, editable=False)
    room = models.ForeignKey('player.Room')
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

    class Meta():
        unique_together = ("music_id", "room")

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
