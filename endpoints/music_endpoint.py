from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from endpoints.utils.decorators import room_required
from music.serializers import MusicSerializer
from music.models import Music
from player.models import Events
from threading import Timer


class Music_endpointView(APIView):
    """
    Music resource.
    """
    @room_required
    def post(self, request, room, format=None):
        """
        Post new music
        ---
        parameters:
          - name: music_id
            type: string
            paramType: body
            required: true

          - name: url
            type: string
            paramType: body
            required: true

          - name: thumbnail
            type: string
            paramType: body
            required: true

          - name: total_duration
            type: integer
            paramType: body
            required: true

          - name: duration
            type: integer
            paramType: body
            required: true

          - name: timer_start
            type: integer
            paramType: body

          - name: source
            type: string
            paramType: body
            required: true

          - name: name
            type: string
            paramType: body
            required: true
        """
        request.data.update({'room_id': room.id})
        try:
            music = Music.objects.get(music_id=request.data.get('music_id'), room=room)
            serializer = MusicSerializer(music, data=request.data, partial=True)
        except Music.DoesNotExist:
            serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            music = serializer.save()
            room.add_music(music)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @room_required
    def patch(self, request, room, pk, format=None):
        """
        Update music
        ---
        serializer: MusicSerializer
        """
        try:
            music = Music.objects.get(pk=pk, room=room)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MusicSerializer(music, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if room.current_music == music:
                Events.get(room).cancel()
                event = Events.set(room, Timer(room.get_current_remaining_time(), room.play_next, ()))
                event.start()
            room.send_update_message()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @room_required
    def delete(self, request, room, pk, format=None):
        """
        Delete a music
        ---
        """
        try:
            music_to_delete = Music.objects.get(pk=pk, room=room)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # We can't delete the current_music (SQL...), then skip the music before deletion
        if music_to_delete == room.current_music:
            room.play_next()
        music_to_delete.delete()
        room.send_update_message()
        return Response(status=status.HTTP_204_NO_CONTENT)
