from constants.match_actions import SUB_OFF, SUB_ON
from django.db.models import Case, When, IntegerField, F, Q, Sum
from django.db.models import Count

from match.models import MatchEvent, LineUp, Match
from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerWeekStats:
    minutes: int
    goals_conceded: int
    goals: int
    assists: int
    own_goal: int
    red_cards: int
    yellow_cards: int
    saves: int
    penalty_misses: int
    penalty_saves: int


class PlayerPointsManager:
    def gameweek_points(self, player, matches_id):
        player_events = MatchEvent.objects.filter(player=player, match_id__in=matches_id)
        player_line_up = LineUp.objects.filter(match_id__in=matches_id, player=player).first()

        player_minutes = self.count_played_minutes(player_events, player_line_up, player.id)
        player_goals_conceded = self.count_goals_conceded(matches_id, player)
        player_stats = self.count_stats(player_events)

    def count_played_minutes(self, events, line_up, player_id):
        if not line_up:
            return 0

        sub_action = SUB_OFF if line_up.in_start else SUB_ON
        sub_event = events.filter(player_id=player_id, action_pk=sub_action).first()

        if line_up.in_start:
            return (sub_event.minutes - 1) if sub_event else 90

        return (90 - sub_event.minutes + 1) if sub_event else 0

    def count_stats(self, events):
        event_counts = events.objects.values('action__code').annotate(count=Count('id'))
        return {item['action__code']: item['count'] for item in event_counts}

    def count_goals_conceded(self, matches_id, player):
        return Match.objects.filter(
            Q(home_club=player.club) | Q(away_club=player.club),
            id__in=matches_id,
        ).aggregate(total_goals=Sum(Case(
            When(home_club=player.club, then=F('away_club_goals')),
            When(away_club=player.club, then=F('home_club_goals')),
            default=0,
            output_field=IntegerField()))
        )['total_goals']

    def insert_gameweek_stats(self, player_id, game_week_id, stats):
        ...
