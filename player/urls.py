# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('player.views',
    url(r'^$', 'login.login', name='login'),
    url(r'^log-out/$', 'login.logout'),

    url(r'^player/$', 'viewer.host.host', name='player'),
    url(r'^remote/$', 'client.home.home', name='remote'),

    # AJAX urls
    url(r'^search-music/$', 'client.library.search_music'),
    url(r'^add-music/$', 'client.library.add_music'),
    url(r'^music_inifite_scroll/$', 'client.library.music_inifite_scroll'),

    url(r'^shuffle/$', 'client.client_player.trigger_shuffle'),
    url(r'^next-music/$', 'client.client_player.next_music'),
    url(r'^dead-link/$', 'client.client_player.next_music'),
    url(r'^volume/$', 'client.client_player.volume_change'),
    url(r'^update-player/$', 'client.client_player.update_player')

)
