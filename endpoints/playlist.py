from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from endpoints.utils.decorators import room_required, pk_required
from music.serializers import PlaylistSerializer
from music.models import PlaylistTrack


class PlaylistView(APIView):
    """
    Playlist resource.
    """
    @room_required
    def get(self, request, room):
        """
        Get current playlist
        ---
        serializer: PlaylistSerializer
        """
        return Response(PlaylistSerializer(room.playlist, many=True).data)

    @pk_required
    @room_required
    def post(self, request, room, pk):
        """
        Update playlist
        ---
        serializer: PlaylistSerializer
        """
        try:
            playlistTrack = PlaylistTrack.objects.get(pk=pk, room=room)
        except PlaylistTrack.DoesNotExist:
            return Response("Can't find this playlistTrack.", status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action not in PlaylistTrack.ACTIONS:
            return Response('Action can only be: "%s"' % '" or "'.join(PlaylistTrack.ACTIONS), status=status.HTTP_400_BAD_REQUEST)

        target = request.data.get('target')
        if action in {'above', 'below'}:
            if target is None:
                return Response('"%s" action needs a target parameter' % action, status=status.HTTP_400_BAD_REQUEST)
            try:
                target = PlaylistTrack.objects.get(pk=int(target), room=room)
            except PlaylistTrack.DoesNotExist:
                return Response("Can't find this playlistTrack as target.", status=status.HTTP_404_NOT_FOUND)

        if target is not None:
            getattr(playlistTrack, action)(target)
        else:
            getattr(playlistTrack, action)()

        message = {
            'action': 'playlistTrack_updated',
            'playlistTracks': PlaylistSerializer(room.playlist.all(), many=True).data
        }
        room.send_message(message)
        return Response(PlaylistSerializer(room.playlist.all(), many=True).data, status=status.HTTP_200_OK)

    @pk_required
    @room_required
    def delete(self, request, room, pk):
        """
        Delete music from playlist
        ---
        serializer: PlaylistSerializer
        """
        try:
            PlaylistTrack.objects.get(pk=pk, room=room).delete()
        except PlaylistTrack.DoesNotExist:
            return Response("Can't find this playlistTrack.", status=status.HTTP_404_NOT_FOUND)

        message = {
            'action': 'playlistTrack_deleted',
            'playlistTracks': PlaylistSerializer(room.playlist.all(), many=True).data
        }
        room.send_message(message)
        return Response(PlaylistSerializer(room.playlist.all(), many=True).data, status=status.HTTP_204_NO_CONTENT)
