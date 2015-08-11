# -*- coding: utf-8 -*-

from rest_framework import serializers

from music.models import Music, TemporaryMusic


class MusicSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    class Meta:
        model = Music
        fields = ('music_id', 'name', 'thumbnail', 'count', 'duration')
