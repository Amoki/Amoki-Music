from django.conf.urls import patterns, url

urlpatterns = patterns('shop.views',
    url(r'^$', 'home'),
    url(r'^nowplaying/$', 'nowplaying'),
)
