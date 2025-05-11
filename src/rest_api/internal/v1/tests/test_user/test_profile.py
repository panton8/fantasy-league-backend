from rest_framework.test import APIClient

from rest_api.testing.api_test_case import ApiTestCase
from rest_api.testing.entity_test_api import EntityTestApi
from team.testing.factories import TeamFactory
from user.testing.factories import UserFactory, UserProfileFactory


class UserProfileTestApi(EntityTestApi):
    entity = 'internal_api:v1:user'


class UserProfileTestCase(ApiTestCase):
    def setUp(self):
        self.profile = UserProfileFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.profile.user)
        self.api = UserProfileTestApi(self.client)

    def test_get_profile_info_without_team__ok(self):
        rsp = self.api.list_get_action('profile')
        self.assertEqual(rsp['email'], self.profile.email)
        self.assertEqual(rsp['budget'], str(self.profile.budget))
        self.assertFalse(rsp['is_team_created'])

    def test_get_profile_info_with_team__ok(self):
        TeamFactory(profile=self.profile)
        rsp = self.api.list_get_action('profile')
        self.assertEqual(rsp['email'], self.profile.email)
        self.assertEqual(rsp['budget'], str(self.profile.budget))
        self.assertTrue(rsp['is_team_created'])
