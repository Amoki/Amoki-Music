import importlib

from django.conf.urls import url

# Load all routes, get the APIView's as_view method
from endpoints.room import RoomNextView
from endpoints import login
from endpoints.sources import sources
views = {}
for endpoint in ['music_endpoint', 'musics', 'room', 'rooms', 'search', 'playlist']:
    views[endpoint] = getattr(importlib.import_module('endpoints.' + endpoint), endpoint.capitalize() + 'View').as_view()

urlpatterns = [
    url(r'^search$', views['search']),
    url(r'^musics$', views['musics']),
    url(r'^music$', views['music_endpoint']),
    url(r'^rooms$', views['rooms']),
    url(r'^room$', views['room']),
    url(r'^room/next$', RoomNextView.as_view()),
    url(r'^sources$', sources),
    url(r'^login$', login.login),
    url(r'^check_credentials$', login.check_credentials),
    url(r'^playlist$', views['playlist']),
]
