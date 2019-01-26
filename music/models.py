import random
import math
from datetime import datetime
from threading import Timer
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
    listeners = models.PositiveIntegerField(editable=False, default=0)

    def __str__(self):
        return f"{self.name} \n playing: {self.current_music}"

    def update(self, modifications):
        for key, value in modifications.items():
            setattr(self, key, value)
            self.save()

    def reset_token(self):
        self.token = generate_token()
        self.save()

    def send_message(self, message):
        """ redis_publisher = RedisPublisher(facility=self.token, broadcast=True)
        message = RedisMessage(json.dumps(message))
        redis_publisher.publish_message(message) """

    def play(self, music):
        # clear the queue
        event = Events.get(self)
        if event:
            event.cancel()

        MusicQueue.objects.create(room=self, music=music)
        self.save()
        print(music.is_valid())
        if not music.is_valid():
            music.delete()
            self.play_next()
        else:
            music.count += 1
            music.last_play = datetime.now()
            music.save()

            """ message = {"action": "play", "room": self.get_serialized_room()}

            self.send_message(message) """

            # Tricky code that create a new thread. Be careful about asynchronousity
            event = Events.set(self, Timer(music.duration, self.play_next, ()))
            event.start()

    def stop(self):
        self.current_music = None
        self.save()
        message = {"action": "stop"}
        self.send_message(message)

    def play_next(self):
        self.refresh_from_db()
        if self.current_music:
            MusicQueue.objects.filter(room=self, music=self.current_music).first().delete()
        next_music = self.music_queue.all().order_by("musicqueue__order").first()
        if next_music:
            self.play(music=next_music)

        elif self.shuffle:
            print("SHUFFLE")
            shuffled = self.select_random_music()
            print(shuffled)
            if shuffled:
                shuffled.date = datetime.now()
                shuffled.save()

                self.play(music=shuffled)

    def add_music(self, music):
        # Adding the music to the queue
        MusicQueue.objects.create(room=self, music=music)

        # Autoplay
        if not self.current_music:
            self.play_next()
        else:
            """ message = {
                "action": "music_added",
                "playlistTracks": self.get_serialized_playlist(),
            }
            self.send_message(message) """

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

    def get_current_remaining_time(self):
        if self.current_music:
            time = self.current_music.duration - int(
                (datetime.now() - self.current_music.last_play).total_seconds()
            )
            return int(time)
        return 0

    def get_remaining_time(self):
        if self.music_queue.count() > 0:
            time_left = (
                self.music_queue.all().aggregate(Sum("duration")).get("duration__sum") or 0
            )
            time_left += self.get_current_remaining_time()
            return int(time_left)
        return 0

    def get_current_time_past(self):
        if self.current_music:
            current_time_past = self.current_music.duration - self.get_current_remaining_time()
            return current_time_past
        return 0

    def get_current_time_past_percent(self):
        if self.current_music:
            try:
                current_total_time = self.current_music.duration
                current_time_left = self.get_current_remaining_time()
                current_time_past_percent = (
                    (current_total_time - current_time_left) * 100
                ) / current_total_time
                return current_time_past_percent
            except ZeroDivisionError:
                pass
        return 0

    def get_musics_remaining(self):
        return self.music_queue.all().order_by("playlisttrack__order")

    def get_count_remaining(self):
        return self.music_queue.count()

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
            self.save()
            if not self.current_music:
                self.play_next()
        else:
            self._shuffle = False
            self.save()


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
