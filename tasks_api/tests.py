from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from tasks_api.models import Project
from users.models import Team


class ProjectAPITestcase(APITestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create(username="nima")
        user.set_password("1234")
        user.save()
        self.project = Project.objects.create(owner=user, title='test')

    def test_create_project(self):
        response = self.client.post(reverse('tasks_api:create_project'), HTTP_AUTHORIZATION='',
                                    data={'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

