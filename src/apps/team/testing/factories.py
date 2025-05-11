from decimal import Decimal
import factory

from core.utils.stringutils import get_random_str_with_length
from team.models import Club, Player, Team, TeamPlayer
from user.testing.factories import UserProfileFactory


class ClubFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    short_name = factory.LazyFunction(lambda: get_random_str_with_length(3).upper())
    code_name = factory.LazyFunction(lambda: get_random_str_with_length(8))
    logo_url = factory.Faker('url')
    t_shirt_logo_url = factory.Faker('url')
    played = 6
    wins = 3
    losses = 2
    draws = 1
    goals_for = 15
    goals_against = 12

    class Meta:
        model = Club


class PlayerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    surname = factory.Faker('last_name')
    club = factory.SubFactory(ClubFactory)
    position = Player.Position.MIDFIELDER
    cost = Decimal('5.7')

    class Meta:
        model = Player


class TeamFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('word')
    profile = factory.SubFactory(UserProfileFactory)
    points = 92

    class Meta:
        model = Team


class TeamPlayerFactory(factory.django.DjangoModelFactory):
    team = factory.SubFactory(TeamFactory)
    player = factory.SubFactory(PlayerFactory)
    is_captain = False
    is_starter = True

    class Meta:
        model = TeamPlayer
