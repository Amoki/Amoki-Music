from rest_framework.generics import ListAPIView

from player.serializers import RoomsSerializer
from player.models import Room


class RoomsView(ListAPIView):
    """
    Rooms resource.
    ---

    """
    queryset = Room.objects.all()
    serializer_class = RoomsSerializer
    paginate_by = 40
    paginate_by_param = 'page_size'
    max_paginate_by = 200

    def get(self, request, *args, **kwargs):
        """
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
            description: Room objects
            type: items
        """
        return super(RoomsView, self).get(request, *args, **kwargs)
