import factory
from django.test import TestCase
from team.services.team_info_manager import TeamInfoManager, PlayerDTO, TeamInfoDTO
from team.testing.factories import TeamFactory, TeamPlayerFactory, PlayerFactory, ClubFactory
from user.testing.factories import UserProfileFactory


class TestTeamInfoManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = TeamInfoManager()

    def setUp(self):
        self.profiles = UserProfileFactory.create_batch(2)
        self.team = TeamFactory(profile=self.profiles[0])
        self.players = PlayerFactory.create_batch(5)
        self.team_players = TeamPlayerFactory.create_batch(5, team=self.team, player=factory.Iterator(self.players))

    def __prepare_team_info_dto(self):
        players = []
        for player in self.players:
            players.append(PlayerDTO(id=player.id, surname=player.surname, position=player.position, is_captain=False, is_starter=True))
        return TeamInfoDTO(name=self.team.name, points=self.team.points, players=players)

    def test_team_info_manager__profile_has_team__ok(self):
        res = self.service.get_line_up(self.profiles[0].id)
        dto = self.__prepare_team_info_dto()

        self.assertEqual(res, dto)

    def test_team_info_manager__profile_without_team__ok(self):
        res = self.service.get_line_up(self.profiles[1].id)

        self.assertIsNone(res)
