from rest_framework import serializers

from player.models import Room
from music.serializers import MusicSerializer


class RoomsSerializer(serializers.ModelSerializer):
    """
    Serializing all the Rooms
    """
    # Get more info about room
    count_left = serializers.IntegerField(source='get_count_remaining', read_only=True)
    time_left = serializers.IntegerField(source='get_remaining_time', read_only=True)
    current_time_left = serializers.IntegerField(source='get_current_remaining_time', read_only=True)
    playlist = serializers.ListField(source='get_musics_remaining', child=MusicSerializer(), read_only=True)
    current_music = MusicSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ('name', 'current_music', 'shuffle', 'can_adjust_volume', 'count_left', 'time_left', 'current_time_left', 'playlist')


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializing one Room
    """
    # Get more info about room
    count_left = serializers.IntegerField(source='get_count_remaining', read_only=True)
    time_left = serializers.IntegerField(source='get_remaining_time', read_only=True)
    token = serializers.CharField(max_length=64, read_only=True)
    current_time_left = serializers.IntegerField(source='get_current_remaining_time', read_only=True)
    playlist = serializers.ListField(source='get_musics_remaining', child=MusicSerializer(), read_only=True)
    current_music = MusicSerializer(read_only=True)

    # Validators for post method
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    name = serializers.CharField(max_length=64, required=True)
    can_adjust_volume = serializers.BooleanField()
    shuffle = serializers.BooleanField(default=False)

    class Meta:
        model = Room
        fields = ('name', 'current_music', 'shuffle', 'can_adjust_volume', 'count_left', 'time_left', 'current_time_left', 'playlist', 'token', 'password')
