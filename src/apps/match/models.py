from django.db.models import UniqueConstraint

from core.django_model.mixins import CreatedUpdatedAt, UuidPk
from django.db import models

from team.models import Club, Player


class GameWeek(CreatedUpdatedAt, UuidPk):
    number = models.PositiveSmallIntegerField()
    actual_from = models.DateTimeField()
    actual_to = models.DateTimeField()

    def __str__(self):
        return f'{self.number}: {self.actual_from} - {self.actual_to}'


class Match(CreatedUpdatedAt, UuidPk):
    gameweek = models.ForeignKey(GameWeek, on_delete=models.CASCADE)
    home_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='home_teams')
    away_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='away_teams')
    home_club_goals = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    away_club_goals = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    start_time = models.DateTimeField()
    full_time = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.start_time}: {self.home_club} - {self.away_club}'


class MatchAction(CreatedUpdatedAt):
    code = models.CharField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    for_display = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MatchEvent(CreatedUpdatedAt, UuidPk):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='events')
    minute = models.PositiveSmallIntegerField()
    additional_minute = models.PositiveSmallIntegerField(default=0)
    action = models.ForeignKey(MatchAction, on_delete=models.CASCADE, related_name='+')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+')


class LineUp(CreatedUpdatedAt, UuidPk):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='line_up')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='appearances')
    in_start = models.BooleanField(default=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['match', 'player'], name='match_unique_player')
        ]
