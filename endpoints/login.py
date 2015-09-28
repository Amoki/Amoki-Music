from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, exceptions

from player.models import Room
from player.serializers import RoomSerializer

from django.conf import settings


@api_view(['GET'])
def login(request):
    """
    Get token
    ---
    serializer: RoomSerializer
    parameters:
      - name: name
        required: true
        type: string
        paramType: query
      - name: password
        required: true
        type: string
        paramType: query

    type:
      room:
        type: Room
        required: true
        description: The room, as /room return it
      websocket:
        type: object
        required: true
        properties:
          heartbeat:
            type: string
            required: true
            description: the websocket heartbeat identifier
          uri:
            type: string
            required: true
            description: the websocket uri to connect
    """
    if not all(k in request.query_params for k in ("name", "password")):
        return Response("Missing name or password parameter", status=status.HTTP_400_BAD_REQUEST)
    try:
        room = Room.objects.get(name=request.query_params['name'], password=request.query_params['password'])
    except Room.DoesNotExist:
        raise exceptions.AuthenticationFailed('Invalid credentials.')

    ws_protocol = request.is_secure() and 'wss://' or 'ws://'

    response = {
        "room": RoomSerializer(room).data,
        "websocket": {
            "heartbeat": settings.WS4REDIS_HEARTBEAT,
            "uri": ws_protocol + request.get_host() + settings.WEBSOCKET_URL
        }
    }

    return Response(response, status=status.HTTP_200_OK)
