from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from endpoints.utils.decorators import room_required, pk_required
from player.serializers import RoomSerializer


class RoomView(APIView):
    """
    Room resource.
    """

    @room_required
    def get(self, request, room, format=None):
        """
        Get current room info
        ---
        serializer: RoomSerializer
        """
        return Response(RoomSerializer(room).data)

    def post(self, request, format=None):
        """
        Post new room
        ---
        serializer: RoomSerializer
        """
        serializer = RoomSerializer(data=request.data)
        # TODO: check we can't update existing room
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @room_required
    def patch(self, request, room, format=None):
        """
        Update current room
        ---
        serializer: RoomSerializer
        """
        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            try:
                room.update(request.data)
            except room.UnableToUpdate as err:
                return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @room_required
    def delete(self, request, room, format=None):
        """
        Delete current room
        """
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomNextView(APIView):
    """
    Next music.
    """

    @pk_required
    @room_required
    def post(self, request, room, pk, format=None):
        """
        Skip music and play next one
        ---
        parameters:
          - name: pk
            required: true
            type: int
            paramType: body
            description: The pk of the current music to be sure to not skip twice the same music
        """
        if not room.current_music:
            return Response("Can't next while no music is currently played", status.HTTP_400_BAD_REQUEST)

        if pk == room.current_music.pk:
            room.play_next()
        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
