import random
import math
from datetime import datetime
from threading import Timer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models import Sum
from django.utils.crypto import get_random_string
from ordered_model.models import OrderedModel

import services


class Music(models.Model):
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=512)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    # Total duration of the music
    total_duration = models.PositiveIntegerField()
    # Duration in second which will be played
    duration = models.PositiveIntegerField()
    # thumbnail in 190 * 120
    thumbnail = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)
    last_play = models.DateTimeField(null=True)
    timer_start = models.PositiveIntegerField(default=0)
    service = models.CharField(max_length=255)
    one_shot = models.BooleanField(default=False)

    class Meta:
        unique_together = ("music_id", "room")

    def __str__(self):
        return """Music : {} \n
                Total duration : {} \n
                Duration : {} \n
                """.format(
            self.name, self.total_duration, self.duration
        )

    def is_valid(self):
        return services.check_validity(self.service, self.music_id)


class MusicQueue(OrderedModel):
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="playlist")
    music = models.ForeignKey("Music", on_delete=models.CASCADE)
    order_with_respect_to = "room"

    ACTIONS = ["top", "up", "down", "bottom", "above", "below"]

    class Meta:
        ordering = ("room", "order")


def generate_token():
    return get_random_string(length=32)


class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    _shuffle = models.BooleanField(default=False)
    token = models.CharField(max_length=64, default=generate_token)
    music_queue = models.ManyToManyField("Music", through="MusicQueue", related_name="+")
    volume = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.name} \n playing: {self.current_music}"

    def update(self, modifications):
        for key, value in modifications.items():
            setattr(self, key, value)
            self.save()

    def reset_token(self):
        self.token = generate_token()
        self.save()

    def play(self, music):
        # clear the queue
        event = Events.get(self)
        if event:
            event.cancel()

        MusicQueue.objects.create(room=self, music=music)
        if not music.is_valid():
            music.delete()
            self.play_next()
        else:
            music.count += 1
            music.last_play = datetime.now()
            music.save()

            # Tricky code that create a new thread. Be careful about asynchronousity
            event = Events.set(self, Timer(music.duration, self.play_next, ()))
            event.start()

    def stop(self):
        self.current_music = None
        self.save()

    def send_state(self):
        from music.serializers import RoomSerializer

        channel_layer = get_channel_layer()
        data = RoomSerializer(self).data
        data["people_count"] = channel_layer.receive_count
        async_to_sync(channel_layer.group_send)(
            f"room_{self.id}", {"type": "room_message", "message": data}
        )

    def play_next(self):
        if self.current_music:
            MusicQueue.objects.filter(room=self, music=self.current_music).first().delete()
        next_music = self.music_queue.all().order_by("musicqueue__order").first()
        if next_music:
            self.play(music=next_music)

        elif self.shuffle:
            shuffled = self.select_random_music()
            if shuffled:
                shuffled.date = datetime.now()
                shuffled.save()
                self.play(music=shuffled)

        self.send_state()

    def add_music(self, music):
        # Adding the music to the queue
        MusicQueue.objects.create(room=self, music=music)

        # Autoplay
        if not self.current_music:
            self.play_next()

    def select_random_music(self):
        # Select random music, excluding 10% last played musics
        musics = (
            self.music_set.exclude(one_shot=True)
            .exclude(duration__gte=600)
            .order_by("-last_play")
        )
        count = musics.count()
        if count <= 1:
            return None
        to_remove = int(count / 10)
        count -= to_remove
        musics = musics[to_remove:]

        a = count / float(5)  # Le point où ca commence à monter
        b = count / float(27)  # La vitesse à laquelle ca monte
        x = random.uniform(1, count - a - 1)
        i = min(
            int(math.floor(x + a - a * math.exp(-x / b))), len(musics) - 1
        )  # Can't select out of range music
        if i < 0:
            i = 0  # Can't get negative index

        return musics[i]

    @property
    def current_music(self):
        return self.music_queue.first()

    @property
    def shuffle(self):
        return self._shuffle

    @shuffle.setter
    def shuffle(self, to_active):
        if self.music_set.count() == 0:
            self._shuffle = False
        elif to_active:
            self._shuffle = True
            if not self.current_music:
                self.play_next()
        else:
            self._shuffle = False


class Events:
    events = dict()

    @classmethod
    def get(cls, room):
        return cls.events[room.name]

    @classmethod
    def set(cls, room, value=None):
        cls.events[room.name] = value
        return value

    @classmethod
    def get_all(cls):
        return cls.events
