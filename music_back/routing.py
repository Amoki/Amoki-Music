from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from music.consumers import ChatConsumer


application = ProtocolTypeRouter(
    {
        # Empty for now (http->django views is added by default)
        "websocket": AuthMiddlewareStack(
            URLRouter([url(r"^ws/chat/(?P<room_name>[^/]+)/$", ChatConsumer)])
        )
    }
)
