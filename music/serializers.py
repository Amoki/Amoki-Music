import time
from django.conf import settings
from rest_framework import serializers
from rest_framework.utils import model_meta
from drf_yasg.utils import swagger_serializer_method
from music.models import Music, Room, MusicQueue


def bind_parents_on_create(Cls):
    class WrappedClass(Cls):
        def create(self, validated_data):
            if hasattr(self, "parent_save_kwargs"):
                kwargs = {
                    self.parent_save_kwargs.get(key, key): value
                    for key, value in self.context["view"].kwargs.items()
                }
            else:
                kwargs = {
                    key.replace("_pk", ""): value
                    for key, value in self.context["view"].kwargs.items()
                }
            info = model_meta.get_field_info(self.Meta.model)
            for field_name, relation_info in info.relations.items():
                if relation_info.related_model and field_name in kwargs:
                    validated_data[f"{field_name}_id"] = kwargs[field_name]
            return super().create(validated_data)

    WrappedClass.__name__ = Cls.__name__
    return WrappedClass


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
    music = MusicSerializer()

    class Meta:
        model = MusicQueue
        fields = ("music",)


class RoomSerializer(serializers.ModelSerializer):
    music_queue = serializers.SerializerMethodField()
    shuffle = serializers.BooleanField(required=False)

    class Meta:
        model = Room
        fields = ("id", "name", "shuffle", "token", "music_queue", "volume")

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
