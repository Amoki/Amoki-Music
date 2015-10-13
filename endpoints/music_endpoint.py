from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from endpoints.utils.decorators import room_required
from music.serializers import MusicSerializer
from music.models import Music


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

          - name: duration
            type: integer
            paramType: body
            required: true

          - name: timer_end
            type: integer
            paramType: body

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
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            music = room.add_music(**serializer.data)
            return Response(MusicSerializer(music).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @room_required
    def patch(self, request, room, pk, format=None):
        """
        Update music
        ---
        serializer: MusicSerializer
        """
        try:
            music = Music.objects.get(pk=pk)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MusicSerializer(music, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @room_required
    def delete(self, request, room, pk, format=None):
        """
        Delete a music
        ---
        """
        try:
            music_to_delete = Music.objects.get(pk=pk)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if music_to_delete == room.current_music:
            room.play_next()
        music_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
