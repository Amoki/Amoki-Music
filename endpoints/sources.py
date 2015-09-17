from rest_framework.generics import ListAPIView

from music.serializers import SourceSerializer
from music.models import Source


class SourcesView(ListAPIView):
    """
    Source resource.
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
