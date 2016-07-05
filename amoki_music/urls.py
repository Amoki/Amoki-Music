from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.conf.urls import include, url
from rest_framework_swagger import urls as rest_framework_swagger_urls
from endpoints import routes
from website.views.home import remote


admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include(admindocs_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include(rest_framework_swagger_urls)),
    url(r'^', include(routes)),
    url(r'^$', remote, name='remote'),
]
