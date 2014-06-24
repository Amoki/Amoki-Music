from django.conf.urls import patterns, url

urlpatterns = patterns('browser.views',
    url(r'^$', 'home'),
    url(r'^nowplaying/$', 'now_playing'),
)
