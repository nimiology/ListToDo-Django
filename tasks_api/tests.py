from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from tasks_api.models import Project
from users.models import Team, MyUser


def UserToken():
    user = MyUser(username='testman', password='1234')
    user.save()
    refresh = RefreshToken.for_user(user)
    return user, f'Bearer {refresh.access_token}'


