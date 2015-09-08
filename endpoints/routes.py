# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# Load all routes, get the APIView's as_view method
endpoints = {}
for endpoint in ['music', 'musics', 'room', 'rooms', 'search']:
    endpoints[endpoint] = __import__(endpoint)[endpoint.capitalize() + 'View'].as_view()

urlpatterns = patterns('website.views',
    url(r'^$', 'login.login.login', name='login'),
    url(r'^log-out/$', 'login.login.logout', name='logout'),

    url(r'^change-ordering/$', 'remote.remote.change_ordering'),

    url(r'^search/$', endpoints['search']),
    url(r'^musics/$', endpoints['musics']),
    url(r'^music/$', endpoints['music']),
    url(r'^rooms/$', endpoints['rooms']),
    url(r'^room/$', endpoints['room']),
)

urlpatterns = format_suffix_patterns(urlpatterns)
