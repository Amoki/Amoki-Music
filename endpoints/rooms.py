from rest_framework.generics import ListAPIView

from player.serializers import RoomsSerializer
from player.models import Room


class RoomsView(ListAPIView):
    """
    Rooms resource.
    ---
    parameters:
        - name: page
            type: int
            paramType: query
    """
    queryset = Room.objects.all()
    serializer_class = RoomsSerializer
    paginate_by = 40
    paginate_by_param = 'page_size'
    max_paginate_by = 200
