
from django.conf import settings
from django.urls import include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core.drf_spectacular.schema_generator import get_schema_generator
from .v1.routers.router import router

urlpatterns = [
    re_path(r'^v1/', include((router.urls, 'v1')))
]


if settings.IS_SWAGGER_ENABLED:
    urlpatterns.extend([
        re_path(r'^docs/schema/$', SpectacularAPIView().as_view(
            urlconf='rest_api.internal.urls',
            generator_class=get_schema_generator(prefix='/api/internal'),
        ), name='api-schema'),
        re_path(r'^docs/swagger/$', SpectacularSwaggerView.as_view(url_name='internal_api:api-schema'), name='swagger-ui'),
    ])
