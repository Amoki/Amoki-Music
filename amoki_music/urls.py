from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^', include('endpoints.routes')),


    url(r'^$', 'website.views.home.remote', name='remote'),
    url(r'^player/$', 'website.views.home.player', name='player'),
)
