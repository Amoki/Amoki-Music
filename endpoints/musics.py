from rest_framework.views import APIView
from endpoints.utils.json_renderer import JSONResponse
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
        return JSONResponse(MusicSerializer(musics, many=True).data)
