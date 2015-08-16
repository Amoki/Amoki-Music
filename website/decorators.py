from functools import wraps
from website.exceptions import AuthenticationFailed

from player.models import Room


def room_required(func):
    @wraps(func)
    def wrap(request, **kwargs):
        try:
            room = Room.objects.get(token=request.session.get('token'))
        except:
            raise AuthenticationFailed()

        return func(request, room=room, **kwargs)
    return wrap
