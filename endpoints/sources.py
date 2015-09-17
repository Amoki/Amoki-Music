from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings


@api_view(['GET'])
def sources(request):
    """
    Get sources list
    ---
    """
    return Response(settings.SOURCES, status=status.HTTP_200_OK)
