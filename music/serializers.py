from rest_framework import serializers

from music.models import Music, Source


class MusicSerializer(serializers.ModelSerializer):
    """
    Serializing all the Music
    """

    # Validators for post method
    name = serializers.CharField(max_length=255, required=True)
    url = serializers.CharField(max_length=512, required=True)
    duration = serializers.IntegerField(required=True)
    room_id = serializers.IntegerField(required=True, write_only=True)
    source_id = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = Music
        fields = ('pk', 'music_id', 'name', 'thumbnail', 'count', 'duration', 'timer_start', 'timer_end', 'url', 'room_id', 'source_id')


class SourceSerializer(serializers.ModelSerializer):
    """
    Serializing all the Source
    """

    class Meta:
        model = Source
        fields = ('pk', 'name')
