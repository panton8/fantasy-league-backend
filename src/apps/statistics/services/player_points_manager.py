from constants.match_actions import SUB_OFF, SUB_ON
from django.db.models import Case, When, IntegerField, F, Q, Sum
from django.db.models import Count

from match.models import MatchEvent, LineUp, Match
from dataclasses import dataclass

from statistics.models import GameWeekStats


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
    def make_gameweek_stats(self, player, matches_id):
        player_events = MatchEvent.objects.filter(player=player, match_id__in=matches_id)
        player_line_up = LineUp.objects.filter(match_id__in=matches_id, player=player).first()

        player_minutes = self.count_played_minutes(player_events, player_line_up, player.id)
        player_goals_conceded = self.count_goals_conceded(matches_id, player)
        player_stats = self.count_stats(player_events)
        player_stats['minutes'] = player_minutes
        player_stats['goals_conceded'] = player_goals_conceded
        stats = self.insert_gameweek_stats(player.id, player_line_up.match.gameweek.id, player_stats)

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
        return GameWeekStats.objects.update_or_create(
            gameweek_id=game_week_id,
            player_id=player_id,
            defaults={
                'goals': stats['goal'],
                'assists': stats['assist'],
                'yellow_cards': stats['yellow_card'],
                'red_cards': stats['red_card'],
                'saves': stats['save'],
                'minutes': stats['minutes'],
                'own_goals': stats['own_goal'],
                'penalties_saved': stats['penalty_save'],
                'penalties_missed': stats['penalty_miss'],
                'goals_conceded': stats['goals_conceded'],
                'clean_sheet': stats['goals_conceded'] == 0,
            }
        )
