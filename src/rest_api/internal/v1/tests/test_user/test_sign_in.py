import json

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.test import APIClient

from rest_api.testing.api_test_case import ApiTestCase
from rest_api.testing.entity_test_api import EntityTestApi
from django.urls import reverse
from user.testing.factories import UserFactory


class UserSignInTestApi(EntityTestApi):
    entity = 'internal_api:v1:user_sign_in'


class UserSignInTestCase(ApiTestCase):

    def setUp(self):
        self.client = APIClient()
        self.api = UserSignInTestApi(self.client)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.password = 'belgium!'
        cls.username = 'eden_hazard'
        cls.user = UserFactory.create(username=cls.username)
        cls.user.set_password(cls.password)
        cls.user.save()

    def test_sign_in__correct_data__ok(self):
        data = {
            'username': self.username,
            'password': self.password,
        }

        rsp = self.api.create_entity(entity_data=data, expected_code=HTTP_200_OK)

        self.assertIsNotNone(rsp['refresh'])
        self.assertIsNotNone(rsp['access'])

    def test_sign_up__incorrect_data__no_account(self):
        data = {
            'username': 'fake_name',
            'password': self.password,
        }

        rsp = self.api.create_entity(entity_data=data, expected_code=HTTP_400_BAD_REQUEST)

        self.assertEqual(rsp[0]['code'], 'user_wrong_credentials')

    def test_refresh_token_user__valid_refresh_token__ok(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.api.create_entity(entity_data=data, expected_code=HTTP_200_OK)
        refresh_token = response['refresh']

        rsp = self.client.post(
                reverse('internal_api:v1:user_refresh_token-list'),
                data={'refresh': refresh_token})
        res = json.loads(rsp.content)

        self.assertEqual(rsp.status_code, HTTP_200_OK)
        self.assertIsNotNone(res['access'])