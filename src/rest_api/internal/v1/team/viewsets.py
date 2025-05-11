from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from rest_api.internal.v1.team.filters import PlayerFilter
from rest_api.internal.v1.team.serializers import PlayerListSerializer, ClubListSerializer, ClubDetailSerializer, \
    TableSerializer, TeamSerializer
from team.models import Player, Team, Club
from team.services.club_position_service import ClubPositionService
from team.services.team_info_manager import TeamInfoManager
from dataclasses import asdict


class ClubViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Club.objects.select_related('club_info').all()
    serializer_class = ClubListSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClubDetailSerializer
        return ClubListSerializer

    @extend_schema(responses={HTTP_200_OK: TableSerializer})
    @action(detail=False, methods=['get'], serializer_class=TableSerializer)
    def table(self, *args, **kwargs):
        clubs_order = ClubPositionService().get_actual_table()
        clubs_data = self.serializer_class(clubs_order, many=True).data
        return Response(status=HTTP_200_OK, data=clubs_data)


class PlayerViewSet(GenericViewSet, ListModelMixin):
    queryset = Player.objects.all()
    serializer_class = PlayerListSerializer
    filterset_class = PlayerFilter
    permission_classes = [AllowAny]


class TeamViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        team_id = serializer.create(data)
        return Response(status=HTTP_201_CREATED, data={'team_id': team_id})

    @action(detail=False, methods=['GET'], url_path='team-info')
    def team_info(self, request, *args, **kwargs):
        profile = self.request.user.profile
        team_info = TeamInfoManager().get_line_up(profile.id)
        return Response(status=HTTP_200_OK, data=asdict(team_info))

