from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import MyUser, Team


def get_user_token(username):
    user = MyUser.objects.create(username=username, password='test')
    refresh = RefreshToken.for_user(user)
    return user, f'Bearer {refresh.access_token}'


class TeamAPITest(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.team = Team.objects.create(name='test', owner=self.user)

    def test_create_team(self):
        response = self.client.post(reverse('users:team_list_create'), data={"name": "test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_teams_list(self):
        response = self.client.get(reverse('users:team_list_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_team(self):
        response = self.client.get(reverse('users:team', kwargs={"pk": self.team.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_team(self):
        response = self.client.patch(reverse('users:team', kwargs={"pk": self.team.pk}), data={'name': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test2')

    def test_put_team(self):
        response = self.client.put(reverse('users:team', kwargs={"pk": self.team.pk}), data={'name': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test2')

    def test_delete_team(self):
        response = self.client.delete(reverse('users:team', kwargs={"pk": self.team.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_join_team(self):
    #     user, token = get_user_token('Jane')
    #     self.client.credentials(HTTP_AUTHORIZATION=token)
    #     response = self.client.post(reverse('users:join_team', kwargs={"inviteSlug": self.team.inviteSlug}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['users'][0]['username'], user.username)


class MyUserListTest(APITestCase):
    def setUp(self) -> None:
        self.user2, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_my_user(self):
        response = self.client.get(reverse('users:my_info'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user2.username)

    def test_my_user_update(self):
        response = self.client.patch(reverse('users:my_info'), data={'first_name': 'John2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllTimeZonesTest(APITestCase):
    def test_all_time_zones_get(self):
        self.user2, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(reverse('users:timezones'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
