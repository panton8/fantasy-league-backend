from core.django_model.mixins import UuidPk, CreatedUpdatedAt
from match.models import GameWeek
from django.db import models

from team.models import Player


class GameWeekStats(UuidPk, CreatedUpdatedAt):
    gameweek = models.ForeignKey(GameWeek, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals = models.PositiveSmallIntegerField(default=0)
    assists = models.PositiveSmallIntegerField(default=0)
    yellow_cards = models.PositiveSmallIntegerField(default=0)
    red_cards = models.PositiveSmallIntegerField(default=0)
    saves = models.PositiveSmallIntegerField(default=0)
    minutes = models.PositiveSmallIntegerField(default=0)
    own_goals = models.PositiveSmallIntegerField(default=0)
    penalties_saved = models.PositiveSmallIntegerField(default=0)
    penalties_missed = models.PositiveSmallIntegerField(default=0)
    goals_conceded = models.PositiveSmallIntegerField(default=0)
    clean_sheet = models.BooleanField(default=False)
