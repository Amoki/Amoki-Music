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
        serializer: MusicSerializer
        """
        request.data['room'] = room.pk
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        serializer: MusicSerializer
        """
        try:
            Music.objects.get(pk=pk).delete()
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
