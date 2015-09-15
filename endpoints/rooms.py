from rest_framework.views import APIView
from rest_framework.response import Response

from player.serializers import RoomsSerializer
from player.models import Room


class RoomsView(APIView):
    """
    Rooms resource.
    """

    def get(self, request, format=None):
        """
        Get rooms
        ---
        serializer: RoomsSerializer
        """
        rooms = Room.objects.all()
        return Response(RoomsSerializer(rooms, many=True).data)
