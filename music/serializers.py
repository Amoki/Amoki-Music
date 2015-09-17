from rest_framework import serializers

from music.models import Music


class MusicSerializer(serializers.ModelSerializer):
    """
    Serializing all the Music
    """
    class Meta:
        model = Music
        fields = ('music_id', 'name', 'thumbnail', 'count', 'duration')
