import datetime
from django.conf import settings
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from music.models import Music, Room, MusicQueue


class MusicSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {"room_pk": "room_id"}

    class Meta:
        model = Music
        fields = (
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


class MusicQueueElement(serializers.Serializer):
    music = MusicSerializer()
    timestamp_start = serializers.IntegerField()


class MusicQueueSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {"room_pk": "room_id"}
    music = MusicSerializer()

    class Meta:
        model = MusicQueue
        fields = ("music",)


class RoomSerializer(serializers.ModelSerializer):
    music_queue = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "name",
            "shuffle",
            "can_adjust_volume",
            "token",
            "music_queue",
            "volume",
            "listeners",
        )

    @swagger_serializer_method(serializer_or_field=MusicQueueElement(many=True))
    def get_music_queue(self, room):
        formatted_queue = []
        music_queue = room.music_queue.all().order_by("musicqueue__order")
        if len(music_queue) >= 1:
            formatted_queue.append(
                {
                    "music": MusicSerializer(music_queue[0].music).data,
                    "timestamp_start": music_queue[0].music.last_play.timestamp(),
                }
            )
            for music_queue_elt, index in enumerate(music_queue[1:]):
                previous_elt = formatted_queue[index]
                formatted_queue.append(
                    {
                        "music": MusicSerializer(music_queue_elt.music).data,
                        "timestamp_start": previous_elt["timestamp_start"]
                        + music_queue_elt.music.duration,
                    }
                )
        return formatted_queue


class RoomReadOnlySerializer(serializers.ModelSerializer):
    current_music = MusicSerializer()

    class Meta:
        model = Room
        fields = ("name", "current_music")


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
