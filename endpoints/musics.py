from rest_framework.views import APIView
from rest_framework.response import Response
from endpoints.utils.decorators import room_required

from music.serializers import MusicSerializer
from music.models import Music


class MusicsView(APIView):
    """
    Musics resource.
    """

    @room_required
    def get(self, request, room, format=None):
        """
        Get musics of the current room
        ---
        serializer: MusicSerializer
        """
        musics = Music.objects.filter(room=room)
        return Response(MusicSerializer(musics, many=True).data)
