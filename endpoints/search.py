from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from endpoints.utils.decorators import room_required

from django.conf import settings

from sources import source


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
            return Response("Missing name or password parameter", status=status.HTTP_400_BAD_REQUEST)

        service = request.query_params['service']
        query = request.query_params['query']

        if service not in settings.SOURCES:
            return Response("This service is not implemented", status=status.HTTP_400_BAD_REQUEST)

        results = source.search(service, query)
        return Response(results)
