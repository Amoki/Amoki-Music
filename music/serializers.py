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
        music = Music(**validated_data)
        music.save()
        return music

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
        Music.objects.filter(pk=instance.pk).update(**validated_data)
        return instance


class PlaylistSerializer(serializers.ModelSerializer):
    """
    Serializing all the Playlist
    """
    music = MusicSerializer(source='track', read_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ('pk', 'order', 'music')
