from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from endpoints.utils.decorators import room_required
from music.serializers import PlaylistSerializer
from music.models import PlaylistTrack


@api_view(['GET'])
@room_required
def get(request, room):
    """
    Get current playlist
    ---
    serializer: PlaylistSerializer
    """
    return Response(PlaylistSerializer(room.playlist, many=True).data)


@api_view(['POST'])
@room_required
def post(request, room, pk, action, target=None):
    """
    Update playlist
    ---
    serializer: PlaylistSerializer
    """
    ACTIONS = ['top', 'up', 'down', 'bottom', 'above', 'below']

    if action in {'above', 'below'} and target is None:
        return Response('"above" or "below" action needs a target parameter', status=status.HTTP_400_BAD_REQUEST)

    if action not in ACTIONS:
        return Response('Action can only be: "%s"' % '" or "'.join(ACTIONS), status=status.HTTP_400_BAD_REQUEST)

    try:
        playlistTrack = PlaylistTrack.objects.get(pk=pk)
    except PlaylistTrack.DoesNotExist:
        return Response("Can't find this playlistTrack.", status=status.HTTP_404_NOT_FOUND)

    if target is not None:
        try:
            playlistTrackTarget = PlaylistTrack.objects.get(pk=target)
            getattr(playlistTrack, action)(playlistTrackTarget)
        except PlaylistTrack.DoesNotExist:
            return Response("Can't find the above or below playlistTrack", status=status.HTTP_404_NOT_FOUND)
    else:
        getattr(playlistTrack, action)()

    room.send_update_message()

    return Response(PlaylistSerializer(room.playlist.all(), many=True).data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@room_required
def delete(request, room, pk, format=None):
    """
    Delete music from playlist
    ---
    serializer: PlaylistSerializer
    """
    try:
        PlaylistTrack.objects.get(pk=pk).delete()
    except PlaylistTrack.DoesNotExist:
        return Response("Can't find this playlistTrack.", status=status.HTTP_404_NOT_FOUND)

    room.send_update_message()
    return Response(PlaylistSerializer(room.playlist.all(), many=True).data, status=status.HTTP_204_NO_CONTENT)
