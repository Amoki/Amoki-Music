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
    try:
        playlistTrack = PlaylistTrack.objects.get(pk=pk, room=room)
    except PlaylistTrack.DoesNotExist:
        return Response("Can't find this playlistTrack.", status=status.HTTP_404_NOT_FOUND)

    if action not in PlaylistTrack.ACTIONS:
        return Response('Action can only be: "%s"' % '" or "'.join(PlaylistTrack.ACTIONS), status=status.HTTP_400_BAD_REQUEST)

    if action in {'above', 'below', 'changetype'}:
        if target is None:
            return Response('"{}" action needs a target parameter'.format(action), status=status.HTTP_400_BAD_REQUEST)
        
        if action == 'changetype':
            if target not in {'NORMAL', 'SHUFFLE'}:
                choices = '; '.join(desc for elem, desc in PlaylistTrack.STATUS_CHOICES)
                return Response('"{}" action needs a target type (can be : {}) parameter'.format(action, choices), status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                target = PlaylistTrack.objects.get(pk=int(target), room=room)
                getattr(playlistTrack, action)(target)
            except PlaylistTrack.DoesNotExist:
                return Response("Can't find this playlistTrack as target.", status=status.HTTP_404_NOT_FOUND)
        
        getattr(playlistTrack, action)(target)
    else:
        getattr(playlistTrack, action)()

    message = {
        'action': 'playlistTrack_updated',
        'playlistTracks': PlaylistSerializer(room.playlist.all(), many=True).data
    }
    room.send_message(message)
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
        p_track = PlaylistTrack.objects.get(pk=pk, room=room)
        p_track_type = p_track.track_type
        p_track.delete()
        if p_track_type == PlaylistTrack.SHUFFLE:
            room.fill_shuffle_playlist()

    except PlaylistTrack.DoesNotExist:
        return Response("Can't find this playlistTrack.", status=status.HTTP_404_NOT_FOUND)

    message = {
        'action': 'playlistTrack_deleted',
        'playlistTracks': PlaylistSerializer(room.playlist.all(), many=True).data
    }
    room.send_message(message)
    return Response(PlaylistSerializer(room.playlist.all(), many=True).data, status=status.HTTP_204_NO_CONTENT)
