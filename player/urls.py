# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('player.views',
    url(r'^$', 'login.login.login', name='login'),
    url(r'^log-out/$', 'login.login.logout'),

    url(r'^player/$', 'player.host.host', name='player'),
    url(r'^remote/$', 'remote.home.home', name='remote'),

    # AJAX urls
    url(r'^search-music/$', 'remote.library.search_music'),
    url(r'^add-music/$', 'remote.library.add_music'),
    url(r'^music_inifite_scroll/$', 'remote.library.music_inifite_scroll'),

    url(r'^shuffle/$', 'remote.remote.trigger_shuffle'),
    url(r'^next-music/$', 'remote.remote.next_music'),
    url(r'^dead-link/$', 'remote.remote.next_music'),
    url(r'^volume/$', 'remote.remote.volume_change'),
    url(r'^update-remote/$', 'remote.remote.update_remote')

)
