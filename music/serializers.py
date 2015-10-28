from rest_framework import serializers

from music.models import Music, PlaylistTrack


class MusicSerializer(serializers.ModelSerializer):
    """
    Serializing all the Music
    """

    # Validators for post method
    name = serializers.CharField(max_length=255, required=True)
    url = serializers.CharField(max_length=512, required=True)
    total_duration = serializers.IntegerField(required=True)
    room_id = serializers.IntegerField(required=True, write_only=True)
    source = serializers.CharField(required=True)

    class Meta:
        model = Music
        fields = ('pk', 'music_id', 'name', 'thumbnail', 'count', 'duration', 'total_duration', 'timer_start', 'timer_end', 'url', 'room_id', 'source', 'last_play')


class PlaylistSerializer(serializers.ModelSerializer):
    """
    Serializing all the Playlist
    """
    music = MusicSerializer(source='track', read_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ('pk', 'order', 'music')
