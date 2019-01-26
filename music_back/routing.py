from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from music.consumers import RoomConsumer


application = ProtocolTypeRouter(
    {
        # Empty for now (http->django views is added by default)
        "websocket": AuthMiddlewareStack(
            URLRouter([url(r"^ws/room/(?P<room_id>[^/]+)/$", RoomConsumer)])
        )
    }
)
