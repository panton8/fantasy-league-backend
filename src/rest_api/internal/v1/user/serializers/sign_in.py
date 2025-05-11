
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from rest_framework import exceptions


class SignInSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        try:
            validated_data = super().validate(attrs)
        except exceptions.AuthenticationFailed:
            raise serializers.ValidationError(
                {'user': 'wrong credentials'},
                code='user_wrong_credentials'
            )

        return validated_data
