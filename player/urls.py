# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('player.views',
    url(r'^$', 'client.home.home'),
    url(r'^player/$', 'host.host'),
    url(r'^log-out/$', 'host.logout'),

    # AJAX urls
    url(r'^search-music/$', 'client.library.search_music'),
    url(r'^add-music/$', 'client.library.add_music'),
    url(r'^music_inifi_scroll/$', 'client.library.music_inifi_scroll'),
    
    url(r'^shuffle/$', 'client.player.trigger_shuffle'),
    url(r'^next-music/$', 'client.player.next_music'),
    url(r'^dead-link/$', 'client.player.next_music'),
    url(r'^volume/$', 'client.player.volume_change'),

)
