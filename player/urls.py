# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('player.views',
    url(r'^$', 'home'),
    url(r'^search-music/$', 'search_music'),
    url(r'^add-music/$', 'add_music'),
    url(r'^dead-link/$', 'dead_link'),
    url(r'^shuffle/$', 'trigger_shuffle'),
    url(r'^next-music/$', 'next_music'),
    url(r'^infinite-scroll/$', 'music_inifi_scroll'),
)
