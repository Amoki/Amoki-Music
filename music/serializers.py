import time
from django.conf import settings
from rest_framework import serializers
from rest_framework.utils import model_meta
from drf_yasg.utils import swagger_serializer_method
from music.models import Music, Room, MusicQueue
from utils.serializers import ScopeLimitedPKRelatedField, bind_parents_on_create


@bind_parents_on_create
class MusicSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {"room_pk": "room_id"}

    class Meta:
        model = Music
        fields = (
            "id",
            "music_id",
            "name",
            "url",
            "room",
            "total_duration",
            "duration",
            "thumbnail",
            "count",
            "last_play",
            "timer_start",
            "service",
            "one_shot",
        )
        read_only_fields = ("room", "count", "last_play")


class MusicQueueElement(serializers.Serializer):
    music = MusicSerializer()
    timestamp_start = serializers.IntegerField()


@bind_parents_on_create
class MusicQueueSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {"room_pk": "room_id"}
    music = MusicSerializer(read_only=True)
    music_id = ScopeLimitedPKRelatedField(write_only=True, parent_lookup_kwargs=parent_lookup_kwargs)

    class Meta:
        model = MusicQueue
        fields = ("music", "music_id")


class RoomSerializer(serializers.ModelSerializer):
    music_queue = serializers.SerializerMethodField()
    shuffle = serializers.BooleanField(required=False)

    class Meta:
        model = Room
        fields = ("id", "name", "shuffle", "music_queue")

    @swagger_serializer_method(serializer_or_field=MusicQueueElement(many=True))
    def get_music_queue(self, room):
        formatted_queue = []
        music_queue = room.music_queue.all().order_by("musicqueue__order")
        if len(music_queue) >= 1:
            formatted_queue.append(
                {
                    "music": MusicSerializer(music_queue[0]).data,
                    "timestamp_start": int(music_queue[0].last_play.timestamp())
                    if music_queue[0].last_play
                    else int(time.time()),
                }
            )
            for index, music_queue_elt in enumerate(music_queue[1:]):
                previous_elt = formatted_queue[index]
                formatted_queue.append(
                    {
                        "music": MusicSerializer(music_queue_elt).data,
                        "timestamp_start": previous_elt["timestamp_start"]
                        + music_queue_elt.duration,
                    }
                )
        return formatted_queue


class RoomReadOnlySerializer(serializers.ModelSerializer):
    current_music = MusicSerializer()

    class Meta:
        model = Room
        fields = ("id", "name", "current_music")


class SearchQuerySerializer(serializers.Serializer):
    service = serializers.ChoiceField(list(settings.SERVICES.items()))
    query = serializers.CharField()


class SearchResultSerializer(serializers.Serializer):
    music_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    channel_name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    thumbnail = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    source = serializers.CharField(read_only=True)
    views = serializers.IntegerField(read_only=True)
    total_duration = serializers.IntegerField(read_only=True)
    duration = serializers.IntegerField(read_only=True)


class CompleteQuerySerializer(serializers.Serializer):
    query = serializers.CharField()
