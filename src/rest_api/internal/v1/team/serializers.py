from django.db.models import Sum
from django.db.transaction import atomic
from rest_framework import serializers
from team.models import Player, TeamPlayer, Team, Club


class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('pk', 'logo_url', 'name')
        model = Club


class ClubDetailSerializer(serializers.ModelSerializer):
    foundation_date = serializers.DateField(source='club_info.foundation_date', format='%Y')
    stadium = serializers.CharField(source='club_info.stadium')
    stadium_capacity = serializers.IntegerField(source='club_info.stadium_capacity')
    info = serializers.CharField(source='club_info.info')
    site_link = serializers.URLField(source='club_info.site_link')

    class Meta:
        fields = ('pk', 'name', 'logo_url', 'foundation_date', 'stadium', 'stadium_capacity', 'info', 'site_link')
        model = Club


class TableSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    goals_diff = serializers.SerializerMethodField()

    class Meta:
        fields = ('pk', 'name', 'logo_url', 'played', 'wins', 'losses', 'draws',
                  'goals_for', 'goals_against', 'points', 'goals_diff')
        model = Club

    def get_points(self, club: Club) -> int:
        return club.wins * 3 + club.draws

    def get_goals_diff(self, club: Club) -> int:
        return club.goals_for - club.goals_against


class PlayerListSerializer(serializers.ModelSerializer):
    club = serializers.CharField(source='club.short_name')
    t_shirt = serializers.URLField(source='club.t_shirt_logo_url')

    class Meta:
        model = Player
        fields = ('id', 'name', 'surname', 'position', 'cost', 'club', 't_shirt')


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    players = serializers.ListField(child=serializers.UUIDField())
    points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'points', 'players', )

    @atomic
    def create(self, validated_data):
        user = self.context.get('user')
        default_name = f'Команда: {user.username}'
        players_ids = validated_data.pop('players', [])
        players = Player.objects.filter(pk__in=players_ids)
        team = Team.objects.create(name=default_name, profile=user.profile)
        position_limits = {
            Player.Position.GOALKEEPER: 1,
            Player.Position.DEFENDER: 4,
            Player.Position.MIDFIELDER: 3,
            Player.Position.FORWARD: 3
        }
        for player in players:
            position_type = player.position
            TeamPlayer.objects.create(
                team=team,
                player=player,
                is_captain=position_type == Player.Position.FORWARD and position_limits[position_type] == 3,
                is_starter=position_limits[position_type] > 0
            )
            position_limits[position_type] -= 1
        profile = user.profile
        total_cost = players.aggregate(total=Sum('cost'))['total']
        profile.budget = profile.budget - total_cost
        profile.save()
        return team.id


class TeamPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPlayer
        fields = ('player', 'is_captain', 'is_starter')
