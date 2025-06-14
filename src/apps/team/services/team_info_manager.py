from typing import List

from django.db.transaction import atomic

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


@dataclass(frozen=True)
class TeamInfoDTO:
    name: str
    points: int
    start_players: List[PlayerDTO]
    bench_players: List[PlayerDTO]


class TeamInfoManager:
    def get_line_up(self, profile_id):
        team = Team.objects.filter(profile_id=profile_id).first()
        if not team:
            return
        team_info = (TeamPlayer.objects
                     .filter(team_id=team.id)
                     .select_related('player', 'team')
                     .values('player_id', 'player__surname', 'player__position', 'is_captain', 'is_starter', 'player__club__t_shirt_logo_url')
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
                )
            )

        return TeamInfoDTO(name=team.name, points=team.points, start_players=start_players, bench_players=bench_players)

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