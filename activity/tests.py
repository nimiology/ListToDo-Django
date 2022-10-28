from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.tests import get_user_token


class ActivityAPITestCase(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_get_activity_list(self):
        response = self.client.get(reverse('activity:activity'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
