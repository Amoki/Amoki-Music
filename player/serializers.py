# -*- coding: utf-8 -*-

from rest_framework import serializers

from player.models import Room
from music.serializers import MusicSerializer


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializing all the Room
    """
    # Get more info about room
    count_left = serializers.IntegerField(source='get_count_remaining', read_only=True)
    time_left = serializers.IntegerField(source='get_remaining_time', read_only=True)
    current_time_left = serializers.IntegerField(source='get_current_remaining_time', read_only=True)
    playlist = serializers.ListField(source='get_musics_remaining', child=MusicSerializer(), read_only=True)

    # Validators for post method
    name = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128)
    can_adjust_volume = serializers.BooleanField()
    shuffle = serializers.BooleanField()

    class Meta:
        model = Room
        fields = ('name', 'current_music', 'shuffle', 'can_adjust_volume', 'count_left', 'time_left', 'current_time_left', 'playlist', 'token')
