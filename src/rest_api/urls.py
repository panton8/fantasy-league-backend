from django.urls import (
    include, re_path,
)

from .internal.urls import urlpatterns as internal_api_urlpatterns

urlpatterns = [
    re_path(r'^internal/', include((internal_api_urlpatterns, 'internal_api'))),
]