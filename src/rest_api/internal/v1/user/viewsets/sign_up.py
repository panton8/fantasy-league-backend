
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import fields
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_api.internal.v1.user.serializers.sign_up import SignUpSerializer


class SignUpViewSet(GenericViewSet, CreateModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    @extend_schema(
        responses={
            HTTP_201_CREATED: inline_serializer(
                name='SignUpResponse',
                fields={
                    'access': fields.CharField(),
                    'refresh': fields.CharField(),
                })
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        user = serializer.instance.user

        refresh_token = TokenObtainPairSerializer.get_token(user)

        return Response({
            'access': str(refresh_token.access_token),
            'refresh': str(refresh_token)
        }, status=HTTP_201_CREATED)
