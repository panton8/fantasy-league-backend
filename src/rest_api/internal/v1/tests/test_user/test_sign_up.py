from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from rest_api.testing.api_test_case import ApiTestCase
from rest_api.testing.entity_test_api import EntityTestApi
from user.models import User, UserProfile
from user.testing.factories import UserFactory


class UserSignUpTestApi(EntityTestApi):
    entity = 'internal_api:v1:user_sign_up'


class UserSignUpTestCase(ApiTestCase):

    def setUp(self):
        self.client = APIClient()
        self.api = UserSignUpTestApi(self.client)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.password = 'belgium!'
        cls.username = 'eden_hazard'

    def test_sign_up__correct_data__user_created(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        self.api.create_entity(entity_data=data)
        user_qs = User.objects.all()
        profile_qs = UserProfile.objects.all()
        user = user_qs.first()
        profile = profile_qs.first()

        self.assertEqual(user_qs.count(), 1)
        self.assertEqual(profile_qs.count(), 1)
        self.assertEqual(user.profile, profile)
        self.assertEqual(user.username, self.username)

    def test_sign_up__duplicate_username__user_not_created(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        UserFactory(username=self.username)
        rsp = self.api.create_entity(entity_data=data, expected_code=HTTP_400_BAD_REQUEST)

        self.assertEqual(rsp[0]['code'], 'username_unique')