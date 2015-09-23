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
        return Music.objects.filter(room=room).order_by('-last_play')

    def get(self, request, *args, **kwargs):
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
        return super(MusicsView, self).get(request, *args, **kwargs)
