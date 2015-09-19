from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, exceptions

from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings

from player.models import Room
from player.serializers import RoomSerializer


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
    """
    if not all(k in request.query_params for k in ("name", "password")):
        return Response("Missing name or password parameter", status=status.HTTP_400_BAD_REQUEST)
    try:
        room = Room.objects.get(name=request.query_params['name'], password=request.query_params['password'])
    except Room.DoesNotExist:
        raise exceptions.AuthenticationFailed('Invalid credentials.')
    except MultiValueDictKeyError:
        return Response("Missing name or password parameter", status=status.HTTP_400_BAD_REQUEST)

    protocol = request.is_secure() and 'wss://' or 'ws://'
    WEBSOCKET_URI = protocol + request.get_host() + settings.WEBSOCKET_URL

    response = {
        'room': RoomSerializer(room).data,
        'ws4redisHeartbeat': settings.WS4REDIS_HEARTBEAT,
        'webSocketUri': WEBSOCKET_URI
    }
    return Response(response, status=status.HTTP_200_OK)
