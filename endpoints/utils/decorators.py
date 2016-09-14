from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from endpoints.utils.authentication import authenticate


def room_required(func):
    @wraps(func)
    def wrap(self, request=None, **kwargs):
        room = authenticate(request)
        return func(self, request, room=room, **kwargs)
    return wrap


def pk_required(func):
    @wraps(func)
    def wrap(self, request=None, **kwargs):
        pk = request.data.get('pk')
        if not pk:
            return Response('{} action needs a pk parameter'.format(request.method), status=status.HTTP_400_BAD_REQUEST)
        return func(self, request, pk=pk, **kwargs)
    return wrap
