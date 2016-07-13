from django.db import models

from ordered_model.models import OrderedModel
from sources import source


class Music(models.Model):
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255, editable=False)
    url = models.CharField(max_length=512, editable=False)
    room = models.ForeignKey('player.Room')
    # Total duration of the music
    total_duration = models.PositiveIntegerField(editable=False)
    # Duration in second which will be played
    duration = models.PositiveIntegerField()
    # thumbnail in 190 * 120
    thumbnail = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0, editable=False)
    last_play = models.DateTimeField(null=True)
    timer_start = models.PositiveIntegerField(default=0)
    source = models.CharField(max_length=255, editable=False)
    one_shot = models.BooleanField(default=False)

    class Meta():
        unique_together = ("music_id", "room")

    def __str__(self):
        return "Title : {}, Total duration : {}, Duration : {}".format(self.name, self.total_duration, self.duration)

    def is_valid(self):
        return source.check_validity(self.source, self.music_id)


class PlaylistTrack(OrderedModel):
    NORMAL = 0
    SHUFFLE = 1
    STATUS_CHOICES = (
        (NORMAL, 'Selected by an user request'),
        (SHUFFLE, 'Randomly selected'),
    )

    room = models.ForeignKey('player.Room', related_name='playlist')
    track = models.ForeignKey('music.Music')
    track_type = models.IntegerField(choices=STATUS_CHOICES, default=NORMAL)
    order_with_respect_to = ('room', 'track_type')

    ACTIONS = ['top', 'up', 'down', 'bottom', 'above', 'below']

    class Meta:
        ordering = ('room', 'track_type', 'order')

    def __str__(self):
        return "Room : {}, Music : {}, Type : {}".format(self.room, self.track, self.track_type)
