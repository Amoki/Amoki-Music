from django.conf import settings

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

API_INFO = openapi.Info(
    title="Coop Music",
    default_version="v1",
    description="Coop Music documentation",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="amoki@amoki.fr"),
    license=openapi.License(name="MIT"),
)

schema_view = get_schema_view(
    public=True, permission_classes=(AllowAny,), url=settings.API_URL
)
