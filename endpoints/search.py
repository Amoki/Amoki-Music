from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from endpoints.utils.decorators import room_required
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from django.conf import settings

from sources import source
from music.models import Music
from music.serializers import MusicSerializer


class SearchView(APIView):
    @room_required
    def get(self, request, room, format=None):
        """
        Get current room info
        ---
        parameters:
          - name: service
            type: string
            paramType: query
            required: true
          - name: query
            type: string
            paramType: query
            required: true
        type:
          duration:
            type: integer
            required: true
            description: time in seconds
          url:
            type: url
            required: true
          name:
            type: string
            required: true
          music_id:
            type: string
            required: true
          thumbnail:
            type: url
            required: true
          source:
            type: string
            required: true
          channel_name:
            type: string
            required: true
          views:
            type: integer
            required: true
        """
        if not all(k in request.query_params for k in ("service", "query")):
            return Response("Missing service or query parameter", status=status.HTTP_400_BAD_REQUEST)

        service = request.query_params['service']
        query = request.query_params['query']

        if service not in settings.SOURCES:
            return Response("This service is not implemented", status=status.HTTP_400_BAD_REQUEST)

        serviceResult = source.search(service, query)
        libraryVideos = []
        for music in Music.objects.filter(room=room):
            if fuzz.token_set_ratio(music.name, query) > 50:
                for serviceMusic in serviceResult :
                    if music.music_id == serviceMusic['music_id'] :
                        serviceResult.remove(serviceMusic)
                libraryVideos.append(MusicSerializer(music).data)
                if len(libraryVideos) >= 10:
                 break

        results = {"serviceSearch": serviceResult, "librarySearch": libraryVideos}
        return Response(results)
