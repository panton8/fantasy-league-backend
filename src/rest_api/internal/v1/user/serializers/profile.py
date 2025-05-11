from rest_framework import serializers

from user.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    is_team_created = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'budget', 'is_team_created', 'username')

    def get_is_team_created(self, profile: UserProfile):
        return getattr(profile, 'team', None) is not None
