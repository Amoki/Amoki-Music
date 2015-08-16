from functools import wraps
from website.exceptions import AuthenticationFailed

from player.models import Room


def room_required(func):
    @wraps(func)
    def wrap(request, **kwargs):
        try:
            room = Room.objects.get(name=request.session.get('room'))
        except:
            raise AuthenticationFailed()

        return func(request, room=room, **kwargs)
    return wrap
