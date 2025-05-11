import factory
from django.test import TestCase

from match.services.match_service import MatchService
from match.testing.factories import MatchFactory, GameWeekFactory


class TestMatchService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = MatchService()

    def setUp(self):
        self.gameweeks = GameWeekFactory.create_batch(2, number=factory.Iterator([1, 2]))
        self.matches = MatchFactory.create_batch(
            3,
            gameweek=factory.Iterator([self.gameweeks[0], self.gameweeks[0], self.gameweeks[1]]),
            full_time=factory.Iterator([True, False, True]),
        )

    def test_match_service__ok(self):
        res = self.service.gameweek_matches(matches=self.matches)
        self.assertEqual(res, 1)

