from typing import List

from django.db.transaction import atomic

from match.services.gameweek_manager import GameweekManager
from statistics.services.player_points_manager import PlayerPointsManager
from team.models import TeamPlayer, Team, Player
from dataclasses import dataclass
from uuid import uuid4
from django.db import models
from django.db.models import Case, When, Value


@dataclass(frozen=True)
class PlayerDTO:
    id: uuid4
    surname: str
    position: str
    is_captain: bool
    t_shirt: str
    cost: float=None


@dataclass(frozen=True)
class PlayerPointsDTO:
    id: uuid4
    surname: str
    position: str
    is_captain: bool
    t_shirt: str
    total_points: int=0
    stats: dict=None


@dataclass(frozen=True)
class TeamInfoDTO:
    name: str
    points: int
    start_players: List[PlayerDTO]
    bench_players: List[PlayerDTO]


@dataclass(frozen=True)
class TeamInfoPointsDTO:
    name: str
    points: int
    start_players: List[PlayerPointsDTO]
    bench_players: List[PlayerPointsDTO]


class TeamInfoManager:
    def get_line_up(self, profile_id):
        team = Team.objects.filter(profile_id=profile_id).first()
        if not team:
            return
        team_info = (TeamPlayer.objects
                     .filter(team_id=team.id)
                     .select_related('player', 'team')
                     .values('player_id', 'player__surname', 'player__position', 'is_captain', 'is_starter', 'player__club__t_shirt_logo_url', 'player__cost')
                     .annotate(
                        status_ordering=Case(
                            When(player__position=Player.Position.GOALKEEPER, then=Value(1)),
                            When(player__position=Player.Position.DEFENDER, then=Value(2)),
                            When(player__position=Player.Position.MIDFIELDER, then=Value(3)),
                            When(player__position=Player.Position.FORWARD, then=Value(4)),
                            output_field=models.PositiveSmallIntegerField(),
                        )))
        start_players = []
        bench_players = []
        for info in team_info:
            if info['is_starter']:
                start_players.append(
                    PlayerDTO(
                        id=info['player_id'],
                        surname=info['player__surname'],
                        position=info['player__position'],
                        is_captain=info['is_captain'],
                        t_shirt=info['player__club__t_shirt_logo_url'],
                        cost=info['player__cost']
                    )
                )
                continue
            bench_players.append(
                PlayerDTO(
                    id=info['player_id'],
                    surname=info['player__surname'],
                    position=info['player__position'],
                    is_captain=info['is_captain'],
                    t_shirt=info['player__club__t_shirt_logo_url'],
                    cost=info['player__cost']
                )
            )

        return TeamInfoDTO(name=team.name, points=team.points, start_players=start_players, bench_players=bench_players)

    def get_line_up_points(self, profile_id):
        team = Team.objects.filter(profile_id=profile_id).first()
        if not team:
            return
        team_info = (TeamPlayer.objects
                     .filter(team_id=team.id)
                     .select_related('player', 'team')
                     .values('player_id', 'player__surname', 'player__position', 'is_captain', 'is_starter', 'player__club__t_shirt_logo_url', 'player__cost')
                     .annotate(
                        status_ordering=Case(
                            When(player__position=Player.Position.GOALKEEPER, then=Value(1)),
                            When(player__position=Player.Position.DEFENDER, then=Value(2)),
                            When(player__position=Player.Position.MIDFIELDER, then=Value(3)),
                            When(player__position=Player.Position.FORWARD, then=Value(4)),
                            output_field=models.PositiveSmallIntegerField(),
                        )))
        start_players = []
        bench_players = []
        team_points = 0
        for info in team_info:
            player_stats = PlayerPointsManager().count_points(actual_gameweek=GameweekManager().get_actual_gameweek(),
                                                              player_id=info['player_id'])
            total_points = 0
            for stat in player_stats.values():
                total_points += stat['points']
            if info['is_starter']:
                start_players.append(
                    PlayerPointsDTO(
                        id=info['player_id'],
                        surname=info['player__surname'],
                        position=info['player__position'],
                        is_captain=info['is_captain'],
                        t_shirt=info['player__club__t_shirt_logo_url'],
                        stats=player_stats,
                        total_points=total_points*2 if info['is_captain'] else total_points
                    )
                )
                team_points += total_points*2 if info['is_captain'] else total_points
                continue
            bench_players.append(
                PlayerPointsDTO(
                    id=info['player_id'],
                    surname=info['player__surname'],
                    position=info['player__position'],
                    is_captain=info['is_captain'],
                    t_shirt=info['player__club__t_shirt_logo_url'],
                    stats=player_stats,
                    total_points=total_points * 2 if info['is_captain'] else total_points
                )
            )
        team.points += team_points
        team.save()
        return TeamInfoPointsDTO(name=team.name, points=team_points, start_players=start_players, bench_players=bench_players)

    @atomic
    def make_sub(self, profile, old_player_id, new_player_id):
        TeamPlayer.objects.filter(team=profile.team, player_id=old_player_id).update(is_starter=False)
        TeamPlayer.objects.filter(team=profile.team, player_id=new_player_id).update(is_starter=True)

    @atomic
    def make_transfer(self, profile, old_player_id, new_player_id):
        old_player_info = TeamPlayer.objects.get(team=profile.team, player_id=old_player_id)
        old_pl_cost = Player.objects.get(id=old_player_id).cost
        new_pl_cost = Player.objects.get(id=new_player_id).cost
        if profile.budget + old_pl_cost - new_pl_cost < 0:
            raise ValueError('Your budget is not enough')
        TeamPlayer.objects.filter(id=old_player_info.id).delete()
        TeamPlayer.objects.create(team=profile.team, player_id=new_player_id, is_captain=old_player_info.is_captain, is_starter=old_player_info.is_starter)

    @atomic
    def change_captain(self,  profile, player_id):
        TeamPlayer.objects.filter(team=profile.team).update(is_captain=False)
        TeamPlayer.objects.filter(team=profile.team, player_id=player_id).update(is_captain=True)
