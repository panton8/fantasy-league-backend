
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle
from rest_framework import fields

from ..serializers.sign_in import SignInSerializer


class SignInViewSet(GenericViewSet, CreateModelMixin, TokenObtainPairView):
    queryset = ''
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer
    throttle_classes = (AnonRateThrottle,)

    @extend_schema(
        responses={
            HTTP_200_OK: inline_serializer(
                name='SignInResponse',
                fields={
                    'access': fields.CharField(),
                    'refresh': fields.CharField(),
                }),
            HTTP_400_BAD_REQUEST:
                OpenApiResponse(description='Response with validation errors'),
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
