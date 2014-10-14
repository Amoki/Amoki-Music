# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('player.views',
    url(r'^$', 'home'),
    url(r'^search-music/$', 'search_music'),
    url(r'^add-music/$', 'add_music'),
    url(r'^lien-mort/$', 'lien_mort'),
    url(r'^shuffle/$', 'trigger_shuffle'),
    url(r'^next-music/$', 'next_music'),
)
