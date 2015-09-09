from functools import wraps

from endpoints.utils.authentication import authenticate


def room_required(func):
    @wraps(func)
    def wrap(self, request, **kwargs):
        room = authenticate(request)
        return func(self, request, room=room, **kwargs)
    return wrap
