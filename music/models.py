from django.db import models

from ordered_model.models import OrderedModel
from sources import source


class Music(models.Model):
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255, editable=False)
    url = models.CharField(max_length=512, editable=False)
    room = models.ForeignKey('player.Room', on_delete=models.CASCADE)
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
        return """Music : {} \n
                Total duration : {} \n
                Duration : {} \n
                """.format(self.name, self.total_duration, self.duration)

    def is_valid(self):
        return source.check_validity(self.source, self.music_id)


class PlaylistTrack(OrderedModel):
    room = models.ForeignKey('player.Room', on_delete=models.CASCADE, related_name='playlist')
    track = models.ForeignKey('music.Music', on_delete=models.CASCADE)
    order_with_respect_to = 'room'

    ACTIONS = ['top', 'up', 'down', 'bottom', 'above', 'below']

    class Meta:
        ordering = ('room', 'order')
