import logging

from huey.contrib.djhuey import db_periodic_task, db_task
from match.models import Match, MatchEvent, LineUp
from match.services.gameweek_manager import GameweekManager
from statistics.services.player_points_manager import PlayerPointsManager
from team.models import Player

logger = logging.getLogger('django')


__all__ = (
    'count_player_gameweek_stats',
)


@db_periodic_task()
def count_players_gameweek_stats():
    actual_gameweek = GameweekManager().get_actual_gameweek()
    matches_id = Match.objects.filter(gameweek=actual_gameweek).values_list('id', flat=True)
    players = Player.objects.all()
    for player in players:
        count_player_gameweek_stats(player.id, matches_id, actual_gameweek.id)


@db_task()
def count_player_gameweek_stats(player_id, matches_id, game_week_id):
    logger.info(f'[PLayer stats] Run task for player_id={player_id}')
    try:
        player = Player.objects.get(id=player_id)
        PlayerPointsManager.make_gameweek_stats(player, matches_id, game_week_id)
    except Exception as exc:
        logger.exception(f'[run_lender_auto_approve] Task exception {exc}')
        return

    logger.debug(f'[run_lender_auto_approve] Finish task for profile_id={player_id}')
