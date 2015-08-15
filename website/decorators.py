from functools import wraps
from django.core.exceptions import PermissionDenied

from player.models import Room


def room_required(func):
    @wraps(func)
    def wrap(request, **kwargs):
        try:
            room = Room.objects.get(name=request.session.get('room'))
        except:
            raise PermissionDenied("Invalid room.")

        return func(request, room=room, **kwargs)
    return wrap
