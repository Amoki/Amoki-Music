from django.conf.urls import patterns, url

urlpatterns = patterns('player.views',
    url(r'^$', 'home'),
)
