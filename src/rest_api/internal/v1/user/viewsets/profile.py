from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from rest_api.internal.v1.user.serializers.profile import UserProfileSerializer
from user.models import UserProfile


class UserProfileViewSet(GenericViewSet):
    def get_object(self):
        return (UserProfile.objects
                .select_related('user')
                .get(user_id=self.request.user))

    @action(methods=['GET'], detail=False, serializer_class=UserProfileSerializer)
    def profile(self, request, *args, **kwargs):
        obj: UserProfile = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(status=HTTP_200_OK, data=serializer.data)
