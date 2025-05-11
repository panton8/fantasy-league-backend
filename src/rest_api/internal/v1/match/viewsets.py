from dataclasses import asdict

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from match.models import Match
from match.services.line_up_manager import LineUpManager
from match.services.match_service import MatchService
from match.services.summary_manager import SummaryManager
from rest_api.internal.v1.match.filters import MatchFilter
from rest_api.internal.v1.match.serializers import GameWeekMatchesSerializer, LineUpSerializer, MatchDetailSerializer


class MatchViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Match.objects.select_related('gameweek').order_by('-gameweek__number', 'start_time')
    serializer_class = GameWeekMatchesSerializer
    permission_classes = [AllowAny]
    filterset_class = MatchFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return GameWeekMatchesSerializer
        elif self.action == 'retrieve':
            return MatchDetailSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        matches = self.filter_queryset(self.get_queryset())
        gameweek_matches = MatchService().gameweek_matches(matches)
        res_data = self.serializer_class(gameweek_matches, many=True).data
        return Response(data=res_data, status=HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='line-up', serializer_class=LineUpSerializer)
    def line_up(self, request, *args, **kwargs):
        match = self.get_object()
        line_up_manager = LineUpManager(match)
        home_line_up_start = line_up_manager.get_home_club_line_up()
        away_line_up_start = line_up_manager.get_away_club_line_up()
        home_line_up_bench = line_up_manager.get_home_club_line_up(in_start=False)
        away_line_up_bench = line_up_manager.get_away_club_line_up(in_start=False)

        home_line_up_start_data = [item['player'] for item in self.get_serializer(home_line_up_start, many=True).data]
        away_line_up_start_data = [item['player'] for item in self.get_serializer(away_line_up_start, many=True).data]
        home_line_up_bench_data = [item['player'] for item in self.get_serializer(home_line_up_bench, many=True).data]
        away_line_up_bench_data = [item['player'] for item in self.get_serializer(away_line_up_bench, many=True).data]

        data = {
            match.home_club.name: {'start': home_line_up_start_data, 'bench': home_line_up_bench_data},
            match.away_club.name: {'start': away_line_up_start_data, 'bench': away_line_up_bench_data},
        }

        return Response(data, status=HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def summary(self, request, *args, **kwargs):
        match = self.get_object()
        summary_manager = SummaryManager(match)
        home_club_summary = summary_manager.get_home_club_summary()
        away_club_summary = summary_manager.get_away_club_summary()

        data = {
            match.home_club.name: [asdict(summary) for summary in home_club_summary],
            match.away_club.name: [asdict(summary) for summary in away_club_summary],
        }

        return Response(data, status=HTTP_200_OK)