from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, exceptions

from django.utils.datastructures import MultiValueDictKeyError

from player.models import Room
from player.serializers import RoomSerializer


@api_view(['GET'])
def login(request):
    """
    Get token
    """
    try:
        room = Room.objects.get(name=request.query_params['name'], password=request.query_params['password'])
    except Room.DoesNotExist:
        raise exceptions.AuthenticationFailed('Invalid credentials.')
    except MultiValueDictKeyError:
        return Response("Missing name or password parameter", status=status.HTTP_400_BAD_REQUEST)
    return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
