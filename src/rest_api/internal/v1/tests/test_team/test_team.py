import factory
from rest_framework.test import APIClient

from rest_api.testing.api_test_case import ApiTestCase
from rest_api.testing.entity_test_api import EntityTestApi
from team.testing.factories import TeamFactory, PlayerFactory, TeamPlayerFactory
from user.testing.factories import UserProfileFactory


class UserTeamTestApi(EntityTestApi):
    entity = 'internal_api:v1:user_team'


class UserTeamTestCase(ApiTestCase):
    def setUp(self):
        self.profile = UserProfileFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.profile.user)
        self.api = UserTeamTestApi(self.client)
        self.team = TeamFactory(profile=self.profile)
        self.players = PlayerFactory.create_batch(5)
        self.team_players = TeamPlayerFactory.create_batch(5, team=self.team, player=factory.Iterator(self.players))

    def __prepare_players_dto(self):
        players = []
        for player in self.players:
            players.append({'id': str(player.id), 'surname': player.surname, 'position': player.position, 'is_captain': False, 'is_starter': True})
        return players

    def test_get_profile_info__ok(self):
        rsp = self.api.list_get_action('team-info')
        players_dto = self.__prepare_players_dto()
        self.assertEqual(rsp['name'], self.team.name)
        self.assertEqual(rsp['points'], self.team.points)
        self.assertEqual(rsp['players'], players_dto)
