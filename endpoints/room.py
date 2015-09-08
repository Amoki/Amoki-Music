from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from endpoints.utils.json_renderer import JSONResponse
from endpoints.utils.decorators import room_required
from player.serializers import RoomSerializer


class RoomView(APIView):
    """
    Get room info or create a new room.
    """
    @room_required
    def get(self, request, room, format=None):
        return JSONResponse(RoomSerializer(room).data)

    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @room_required
    def patch(self, request, room, format=None):
        serializer = RoomSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @room_required
    def delete(self, request, room, format=None):
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
