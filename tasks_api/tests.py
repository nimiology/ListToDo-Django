from django.contrib.auth.models import User
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


class ProjectAPITest(APITestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(title='test', owner=user,
                                              team=team)


user.delete()
