# -*- coding: utf-8 -*-
import importlib

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# Load all routes, get the APIView's as_view method
views = {}
for endpoint in ['music', 'musics', 'room', 'rooms', 'search']:
    views[endpoint] = getattr(importlib.import_module('endpoints.' + endpoint), endpoint.capitalize() + 'View').as_view()


urlpatterns = patterns('endpoints.routes',
    url(r'^search$', views['search']),
    url(r'^musics$', views['musics']),
    url(r'^music$', views['music']),
    url(r'^rooms$', views['rooms']),
    url(r'^room$', views['room']),
)

urlpatterns = format_suffix_patterns(urlpatterns)
