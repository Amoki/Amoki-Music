from rest_framework import serializers

from music.models import Music, PlaylistTrack
from player.models import Events
from threading import Timer


class MusicSerializer(serializers.ModelSerializer):
    """
    Serializing all the Music
    """

    # Validators for post method
    name = serializers.CharField(max_length=255, required=True)
    url = serializers.CharField(max_length=512, required=True)
    total_duration = serializers.IntegerField(required=True)
    duration = serializers.IntegerField(required=True)
    room_id = serializers.IntegerField(required=True, write_only=True)
    source = serializers.CharField(required=True)

    class Meta:
        model = Music
        fields = ('pk', 'music_id', 'name', 'thumbnail', 'count', 'duration', 'total_duration', 'timer_start', 'url', 'room_id', 'source', 'last_play')

    def create(self, validated_data):
        """
            Override the default Serializer.save() method
            =============================================

            create(..) is called if we don't pass an existing music to the Serializer
            update(..) method NEED to be implemented too !

            :param self: Instance param
            :param validated_data: A dict of validated data from the Serializer
            :type self: MusicSerializer
            :type validated_data: dict
            :return: The Music object CREATED with the valid data from the Serializer
            :rtype: Music
        """
        return Music.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
            Override the default Serializer.save() method
            =============================================

            update(..) is called if we pass an existing music to the Serializer
            create(..) method NEED to be implemented too !

            :param self: Instance param
            :param instance: The Music instance given to the Serializer
            :param validated_data: A dict of validated data from the Serializer
            :type self: MusicSerializer
            :type instance: Music
            :type validated_data: dict
            :return: The Music object UPDATED with the valid data from the Serializer
            :rtype: Music
        """
        music = Music.objects.filter(pk=instance.pk)
        music.update(**validated_data)
        music = music.first()
        room = instance.room
        if room.current_music == music:
            Events.get(room).cancel()
            event = Events.set(room, Timer(room.get_current_remaining_time(), room.play_next, ()))
            event.start()
        return music


class PlaylistSerializer(serializers.ModelSerializer):
    """
    Serializing all the Playlist
    """
    music = MusicSerializer(source='track', read_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ('pk', 'order', 'music')
