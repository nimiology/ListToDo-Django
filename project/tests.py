from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project.models import Project, ProjectUser
from users.tests import get_user_token


class ProjectAPITestCase(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.project = Project.objects.create(owner=self.user)

    def test_create_project(self):
        response = self.client.post(reverse('project:projects_list'), data={'title': 'test', })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_projects_list(self):
        response = self.client.get(reverse('project:projects_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project(self):
        response = self.client.get(reverse('project:project', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('project:project', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_project(self):
        response = self.client.delete(reverse('project:project', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('project:project', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_project(self):
        response = self.client.put(reverse('project:project', kwargs={'pk': self.project.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_put_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('project:project', kwargs={'pk': self.project.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_project(self):
        response = self.client.patch(reverse('project:project', kwargs={'pk': self.project.pk}),
                                     data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_patch_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('project:project', kwargs={'pk': self.project.pk}),
                                     data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_project_invite_slug(self):
        response = self.client.get(reverse('project:change_invite_slug', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_project_invite_slug_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('project:change_invite_slug', kwargs={'pk': self.project.pk}), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_join_to_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(
            reverse('project:join_to_project', kwargs={'invite_slug': self.project.invite_slug}), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('project:leave_project', kwargs={
            'pk': ProjectUser.objects.create(owner=user, project=self.project).project.pk}), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('project:leave_project', kwargs={
            'pk': self.project.pk}), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_personalize_project_put(self):
        response = self.client.put(
            reverse('project:personalize_project', kwargs={'pk': self.project.users.get(owner=self.user).pk}),
            data={'color': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_personalize_project_patch(self):
        response = self.client.patch(
            reverse('project:personalize_project', kwargs={'pk': self.project.users.get(owner=self.user).pk}),
            data={'color': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_personalize_project_put_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(
            reverse('project:personalize_project', kwargs={'pk': self.project.users.get(owner=self.user).pk}),
            data={'color': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_personalize_project_patch_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(
            reverse('project:personalize_project', kwargs={'pk': self.project.users.get(owner=self.user).pk}),
            data={'color': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_position(self):
        for i in range(100):
            Project.objects.create(owner=self.user, title="project")
        request = self.client.patch(
            reverse('project:personalize_project', kwargs={'pk': self.project.users.get(owner=self.user).pk}),
            data={'position': 51})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['position'], 51)
        request = self.client.patch(
            reverse('project:personalize_project', kwargs={'pk': self.project.users.get(owner=self.user).pk}),
            data={'position': 10})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['position'], 10)
