from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_nested import routers
from music.views import (
    MusicViewSet,
    RoomViewSet,
    RoomListViewSet,
    MusicQueueViewSet,
    search_view,
    time_view,
)
from utils.doc import schema_view

router = routers.SimpleRouter(trailing_slash=False)
router.register("rooms", RoomViewSet)
router.register("room-list", RoomListViewSet)

rooms_router = routers.NestedSimpleRouter(router, "rooms", lookup="room")
rooms_router.register("musics", MusicViewSet)
rooms_router.register("queue", MusicQueueViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("", include(router.urls)),
    path("", include(rooms_router.urls)),
    path("search", search_view),
    path("time", time_view),
    url(
        r"^doc(?P<format>.json|.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(r"^doc$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
