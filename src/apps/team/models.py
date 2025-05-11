from core.django_model.mixins import UuidPk, CreatedUpdatedAt
from django.db import models

from user.models import UserProfile


class Club(CreatedUpdatedAt):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=3)
    code_name = models.CharField(primary_key=True, max_length=255, unique=True)
    logo = models.FileField(upload_to=f'club_logo/', null=True, blank=True)
    logo_url = models.URLField()
    t_shirt_logo = models.FileField(upload_to=f't_shirt_logo/', null=True, blank=True)
    t_shirt_logo_url = models.URLField()
    played = models.PositiveSmallIntegerField(default=0)
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    draws = models.PositiveSmallIntegerField(default=0)
    goals_for = models.PositiveSmallIntegerField(default=0)
    goals_against = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class ClubInfo(CreatedUpdatedAt):
    club = models.OneToOneField(Club, on_delete=models.CASCADE, related_name='club_info')
    foundation_date = models.DateField()
    stadium = models.CharField(max_length=255)
    stadium_capacity = models.PositiveIntegerField(default=1000)
    info = models.TextField()
    site_link = models.URLField()


class Player(UuidPk, CreatedUpdatedAt):
    class Position(models.TextChoices):
        GOALKEEPER = 'gkp', 'GKP'
        DEFENDER = 'def', 'DEF'
        MIDFIELDER = 'mid', 'MID'
        FORWARD = 'fwd', 'FWD'
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    position = models.CharField(max_length=255, choices=Position.choices)
    t_short_number = models.PositiveSmallIntegerField(null=True, blank=True)
    card_image_link = models.URLField(null=True, blank=True)
    card_image = models.FileField(upload_to=f'players/', null=True, blank=True)
    cost = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.name} {self.surname} ({self.position}) - {self.club}'

    def name_to_display(self):
        return f'{self.name[0]}. {self.surname}'


class Team(UuidPk, CreatedUpdatedAt):
    name = models.CharField(max_length=255)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='team')
    players = models.ManyToManyField(
        Player,
        through='TeamPlayer',
        related_name='teams'
    )
    points = models.PositiveSmallIntegerField(default=0)


class TeamPlayer(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    is_captain = models.BooleanField()
    is_starter = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'player'], name='team_player_unique')
        ]
