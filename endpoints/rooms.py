from rest_framework.views import APIView
from endpoints.utils.json_renderer import JSONResponse

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
        return JSONResponse(RoomsSerializer(rooms, many=True).data)
