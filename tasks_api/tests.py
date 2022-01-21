from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from tasks_api.models import Project
from users.models import Team

user = User.objects.create(username='test_man1',
                           email='test_man1@mail.com',
                           password='1234')
user2 = User.objects.create(username='test_man2',
                            email='test_man2@mail.com',
                            password='1234')
team = Team.objects.create(name='test_team',
                           owner=user)
team.users.add(user2)
refresh = RefreshToken.for_user(user)
access_token = str(refresh.access_token)


class ProjectAPITestcase(APITestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(owner=user, title='test', team=team)

    def test_create_project(self):
        response = self.client.post(reverse('tasks_api:create_project'), HTTP_AUTHORIZATION=access_token,
                                    data={'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


user.delete()
user2.delete()