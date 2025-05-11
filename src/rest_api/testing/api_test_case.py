
from django.test import TestCase
from rest_framework.test import APIClient


class ApiTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        ...

    def setUp(self):
        super().setUp()
        self.client = APIClient()
