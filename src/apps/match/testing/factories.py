import factory
from datetime import datetime
from match.models import Match, GameWeek
from team.testing.factories import ClubFactory


class GameWeekFactory(factory.django.DjangoModelFactory):
    number = 1
    actual_from = datetime(2025, 4, 10, 17)
    actual_to = datetime(2025, 4, 15, 00)

    class Meta:
        model = GameWeek


class MatchFactory(factory.django.DjangoModelFactory):
    gameweek = factory.SubFactory(GameWeekFactory)
    home_club = factory.SubFactory(ClubFactory)
    away_club = factory.SubFactory(ClubFactory)
    home_club_goals = 1
    away_club_goals = 3
    start_time = datetime(2025, 4, 17, 18, 0)
    full_time = True

    class Meta:
        model = Match
