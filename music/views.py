from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_nested.viewsets import NestedViewSetMixin
from drf_yasg.utils import swagger_auto_schema

from music.serializers import (
    MusicSerializer,
    RoomSerializer,
    RoomReadOnlySerializer,
    MusicQueueSerializer,
    SearchQuerySerializer,
    SearchResultSerializer,
)
from music.models import Room, Music, MusicQueue
import services


class RoomListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomReadOnlySerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MusicViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class MusicQueueViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = MusicQueue.objects.all()
    serializer_class = MusicQueue

    @action(detail=False, methods=["post"])
    def next(self, request, pk):
        room = Room.objects.get(id=self.kwargs.get("room_pk"))
        room.play_next()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def top(self, request, pk):
        music_queue_element = self.get_object()
        music_queue_element.top()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def up(self, request, pk):
        music_queue_element = self.get_object()
        music_queue_element.up()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def down(self, request, pk):
        music_queue_element = self.get_object()
        music_queue_element.down()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def bottom(self, request, pk):
        music_queue_element = self.get_object()
        music_queue_element.bottom()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # TODO: add above and below methods


class SearchView(APIView):
    @swagger_auto_schema(
        query_serializer=SearchQuerySerializer,
        responses={200: SearchResultSerializer(many=True)},
    )
    def get(self, request, format=None):
        serializer = SearchQuerySerializer(request.query_string)
        serializer.is_valid(raise_exception=True)
        results = services.search(**serializer.validated_data)
        return Response(results)
