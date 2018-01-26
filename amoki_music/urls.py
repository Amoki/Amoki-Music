from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.conf.urls import include, url
from rest_framework_swagger.views import get_swagger_view
from endpoints import routes
from website.views.home import remote

schema_view = get_swagger_view(title='Music API')


admin.autodiscover()


urlpatterns = [
    url(r'^admin/doc/', include(admindocs_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', schema_view),
    url(r'^', include(routes)),
    url(r'^$', remote, name='remote'),
]
