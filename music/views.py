import time
import requests
from rest_framework import viewsets, mixins, status, views, serializers
from rest_framework.decorators import action, api_view
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
    CompleteQuerySerializer,
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

    def perform_create(self, serializer):
        music = serializer.save()
        music.room.add_music(music)


class MusicQueueViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = MusicQueue.objects.all()
    serializer_class = MusicQueueSerializer

    @action(detail=False, methods=["post"])
    def next(self, request, room_pk):
        room = Room.objects.get(id=room_pk)
        room.stop_current_music()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def top(self, request, room_pk):
        music_queue_element = self.get_object()
        music_queue_element.top()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def up(self, request, room_pk):
        music_queue_element = self.get_object()
        music_queue_element.up()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def down(self, request, room_pk):
        music_queue_element = self.get_object()
        music_queue_element.down()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def bottom(self, request, room_pk):
        music_queue_element = self.get_object()
        music_queue_element.bottom()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # TODO: add above and below methods


@swagger_auto_schema(
    query_serializer=CompleteQuerySerializer,
    responses={200: serializers.ListSerializer(child=serializers.CharField())},
    method="GET",
)
@api_view(["GET"])
def complete_view(request):
    serializer = CompleteQuerySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    params = {
        "hl": "fr",  # Language
        "ds": "yt",  # Restrict lookup to youtube
        "q": serializer.validated_data["query"],  # query term
        "client": "firefox",  # force youtube style response, i.e. json
    }
    response = requests.get("https://suggestqueries.google.com/complete/search", params=params)
    response.raise_for_status()
    results = response.json()[1]
    return Response(results)


@swagger_auto_schema(
    query_serializer=SearchQuerySerializer,
    responses={200: SearchResultSerializer(many=True)},
    method="GET",
)
@api_view(["GET"])
def search_view(request):
    serializer = SearchQuerySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    results = services.search(**serializer.validated_data)
    return Response(results)


@api_view(["GET"])
def time_view(request):
    data = {"server_time": int(time.time())}
    return Response(data, status=status.HTTP_200_OK)
