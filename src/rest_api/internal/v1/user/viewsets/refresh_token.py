
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ViewSetMixin
from rest_framework_simplejwt.views import TokenRefreshView


__all__ = (
    'RefreshTokenViewSet',
)


class RefreshTokenViewSet(CreateModelMixin, ViewSetMixin, TokenRefreshView):
    def create(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
