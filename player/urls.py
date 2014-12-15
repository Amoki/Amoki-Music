# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('player.views',
    url(r'^$', 'client.home'),
    url(r'^player/$', 'host.host'),
    url(r'^log-out/$', 'host.logout'),

    # AJAX urls
    url(r'^search-music/$', 'client.search_music'),
    url(r'^add-music/$', 'client.add_music'),
    url(r'^dead-link/$', 'client.dead_link'),
    url(r'^shuffle/$', 'client.trigger_shuffle'),
    url(r'^next-music/$', 'client.next_music'),
    url(r'^volume/$', 'client.volume_change'),
)
