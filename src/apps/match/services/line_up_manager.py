from django.db import models
from django.db.models import Case, When, Value

from match.models import Match, LineUp
from team.models import Player


class LineUpManager:
    def __init__(self, match: Match):
        self.match = match

    def get_home_club_line_up(self, in_start: bool=True):
        qs = LineUp.objects \
            .select_related('player__club') \
            .filter(match=self.match, player__club=self.match.home_club, in_start=in_start) \
            .annotate(
                status_ordering=Case(
                    When(player__position=Player.Position.GOALKEEPER, then=Value(1)),
                    When(player__position=Player.Position.DEFENDER, then=Value(2)),
                    When(player__position=Player.Position.MIDFIELDER, then=Value(3)),
                    When(player__position=Player.Position.FORWARD, then=Value(4)),
                    output_field=models.PositiveSmallIntegerField(),
            )
        )

        return qs.order_by('status_ordering')

    def get_away_club_line_up(self, in_start: bool=True):
        qs = LineUp.objects \
            .select_related('player__club') \
            .filter(match=self.match, player__club=self.match.away_club, in_start=in_start) \
            .annotate(
                status_ordering=Case(
                    When(player__position=Player.Position.GOALKEEPER, then=Value(1)),
                    When(player__position=Player.Position.DEFENDER, then=Value(2)),
                    When(player__position=Player.Position.MIDFIELDER, then=Value(3)),
                    When(player__position=Player.Position.FORWARD, then=Value(4)),
                    output_field=models.PositiveSmallIntegerField(),
                )
        )

        return qs.order_by('status_ordering')
