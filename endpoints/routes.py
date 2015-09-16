# -*- coding: utf-8 -*-
import importlib

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# Load all routes, get the APIView's as_view method
views = {}
for endpoint in ['music_endpoint', 'musics', 'room', 'rooms', 'search', 'sources']:
    views[endpoint] = getattr(importlib.import_module('endpoints.' + endpoint), endpoint.capitalize() + 'View').as_view()
from endpoints.room import RoomNextView

urlpatterns = patterns('endpoints.routes',
    url(r'^search$', views['search']),
    url(r'^musics$', views['musics']),
    url(r'^music$', views['music_endpoint']),
    url(r'^music/(?P<pk>[0-9]+)$', views['music_endpoint']),
    url(r'^rooms$', views['rooms']),
    url(r'^room$', views['room']),
    url(r'^room/next$', RoomNextView.as_view()),
    url(r'^sources$', views['sources']),
)

urlpatterns = format_suffix_patterns(urlpatterns)
