from rest_framework.generics import ListAPIView
from endpoints.utils.decorators import room_required

from music.serializers import MusicSerializer
from music.models import Music


class MusicsView(ListAPIView):
    """
    Musics resource.
    """
    serializer_class = MusicSerializer
    paginate_by = 40
    paginate_by_param = 'page_size'
    max_paginate_by = 200

    @room_required
    def get_queryset(self, request, room):
        """
        Get musics of the current room
        ---
        serializer: MusicSerializer
        parameters:
        - name: page
            type: int
            paramType: query
        """
        return Music.objects.filter(room=room)
