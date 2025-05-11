from match.models import Match, LineUp
from rest_framework import serializers
from rest_api.internal.v1.team.serializers import ClubListSerializer
from team.models import Player


class MatchDetailSerializer(serializers.ModelSerializer):
    home_club = serializers.CharField(source='home_club.name')
    away_club = serializers.CharField(source='away_club.name')
    home_club_logo = serializers.CharField(source='home_club.logo_url')
    away_club_logo = serializers.CharField(source='away_club.logo_url')

    class Meta:
        model = Match
        fields = ('home_club', 'away_club', 'home_club_goals', 'away_club_goals', 'home_club_logo', 'away_club_logo',  'start_time', 'full_time')


class MatchSerializer(serializers.ModelSerializer):
    home_club = ClubListSerializer()
    away_club = ClubListSerializer()

    class Meta:
        model = Match
        fields = ('id', 'home_club', 'away_club', 'home_club_goals', 'away_club_goals', 'start_time', 'full_time')


class GameWeekMatchesSerializer(serializers.Serializer):
    gameweek = serializers.IntegerField()
    matches = MatchSerializer(many=True)

    class Meta:
        fields = ('gameweek', 'matches')


class PlayerSerializer(serializers.ModelSerializer):
    club = serializers.CharField(source='club.name', read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'name', 'surname', 'club', 'position')


class PlayerLineUpSerializer(PlayerSerializer):
    team = None
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'display_name', 'position', 't_short_number', 'card_image_link')

    def get_display_name(self, obj: Player) -> str:
        return f'{obj.name[0]}.{obj.surname}'


class LineUpSerializer(serializers.ModelSerializer):
    player = PlayerLineUpSerializer()

    class Meta:
        model = LineUp
        fields = ('player', )
