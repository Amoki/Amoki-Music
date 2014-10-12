# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('player.views',
    url(r'^$', 'home'),
	url(r'^test-post/$', 'test_post'),
)
