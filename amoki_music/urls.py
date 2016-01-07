from django.conf.urls import include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^', include('endpoints.routes')),

    url(r'^$', 'website.views.home.remote', name='remote'),
]
