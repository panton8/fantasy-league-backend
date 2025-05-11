from decimal import Decimal

import factory

from user.models import User, UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')

    class Meta:
        model = User


class UserProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    email = factory.Faker('email')
    budget = Decimal('100.00')

    class Meta:
        model = UserProfile
