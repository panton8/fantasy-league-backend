from constants.match_actions import SUB_OFF, SUB_ON
from django.db.models import Case, When, IntegerField, F, Q, Sum
from django.db.models import Count

from match.models import MatchEvent, LineUp, Match
from dataclasses import dataclass

from statistics.models import GameWeekStats
from team.models import Player


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

    def count_points(self, actual_gameweek, player_id):
        stats = GameWeekStats.objects.filter(gameweek=actual_gameweek, player_id=player_id).first()
        if not stats:
            return {
            'goal': {'count': 0, 'points': 0},
            'assist': {'count': 0, 'points': 0},
            'yellow_card': {'count': 0, 'points': 0},
            'red_card': {'count': 0, 'points': 0},
            'save': {'count': 0, 'points': 0},
            'minute': {'count': 0, 'points': 0},
            'own_goal': {'count': 0, 'points': 0},
            'penalty_saved': {'count': 0, 'points': 0},
            'penalty_missed':{'count': 0, 'points': 0},
            'goals_conceded': {'count': 0, 'points': 0},
        }
        goal_points = self.__count_goal_points(stats.goals, stats.player.position)
        assists_points = self.__count_assists_points(stats.assists)
        yellow_cards_points = self.__count_yellow_cards_points(stats.yellow_cards)
        red_cards_points = self.__count_red_cards_points(stats.red_cards)
        saves_points = self.__count_saves_points(stats.saves)
        minutes_points = self.__count_minutes_points(stats.minutes)
        own_goal_points = self.__count_own_goal_points(stats.own_goals)
        penalty_save_points = self.__count_penalties_saves_points(stats.penalties_saved)
        penalty_miss_points = self.__count_penalties_misses_points(stats.penalties_missed)
        clean_sheet_points = self.__count_clean_sheet_points(stats.clean_sheet, stats.player.position)
        return {
            'goal': {'count': stats.goals, 'points': goal_points},
            'assist': {'count': stats.assists, 'points': assists_points},
            'yellow_card': {'count': stats.yellow_cards, 'points': yellow_cards_points},
            'red_card': {'count': stats.red_cards, 'points': red_cards_points},
            'save': {'count': stats.saves, 'points': saves_points},
            'minute': {'count': stats.minutes, 'points': minutes_points},
            'own_goal': {'count': stats.own_goals, 'points': own_goal_points},
            'penalty_saved': {'count': stats.penalties_saved, 'points': penalty_save_points},
            'penalty_missed':{'count': stats.penalties_missed, 'points': penalty_miss_points},
            'goals_conceded': {'count': stats.goals_conceded, 'points': clean_sheet_points if stats.minutes else 0},
        }

    def __count_goal_points(self, count, position):
        match position:
            case Player.Position.FORWARD:
                return count * 4
            case Player.Position.MIDFIELDER:
                return count * 5
            case Player.Position.DEFENDER:
                return count * 6
            case Player.Position.GOALKEEPER:
                return count * 10

    def __count_assists_points(self, count):
        return count * 3

    def __count_yellow_cards_points(self, count):
        return count * -1

    def __count_red_cards_points(self, count):
        return count * -3

    def __count_saves_points(self, count):
        return count // 3

    def __count_minutes_points(self, count):
        if count == 0:
            return 0
        if count < 60:
            return 1
        return 2

    def __count_own_goal_points(self, count):
        return count * -2

    def __count_penalties_saves_points(self, count):
        return count * -5

    def __count_penalties_misses_points(self, count):
        return count * -2

    def __count_clean_sheet_points(self, clean_sheet, position):
        if not clean_sheet:
            return 0
        match position:
            case Player.Position.MIDFIELDER:
                return 1
            case Player.Position.FORWARD:
                return 0
            case _:
                return 4
