from functools import wraps

from endpoints.utils.authentication import authenticate


def room_required(func):
    @wraps(func)
    def wrap(self, request=None, **kwargs):
        # Sometimes (on /playlist queries), there is no request but seff is the request
        if not request:
            request = self
            self = None
        room = authenticate(request)
        if not self:
            return func(request, room=room, **kwargs)
        return func(self, request, room=room, **kwargs)
    return wrap
