from rest_framework.generics import ListAPIView
from endpoints.utils.decorators import room_required
from endpoints.utils.paginators import StandardResultsSetPagination

from music.serializers import MusicSerializer
from music.models import Music


class MusicsView(ListAPIView):
    """
    Musics resource.
    """
    serializer_class = MusicSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Music.objects.filter(room=self.room).order_by('-last_play')

    @room_required
    def get(self, request, room, *args, **kwargs):
        """
        Get musics of the current room
        ---
        parameters:
          - name: page
            type: integer
            paramType: query
          - name: page_size
            type: integer
            paramType: query

        type:
          count:
            required: true
            type: integer
          next:
            required: true
            type: url
          previous:
            required: true
            type: url
          results:
            required: true
            description: Music objects
            type: items
        """
        self.room = room
        return super(MusicsView, self).get(request, *args, **kwargs)
