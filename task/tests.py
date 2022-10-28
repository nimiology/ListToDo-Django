from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project.models import Project
from section.models import Section
from task.models import Task
from users.tests import get_user_token


class TaskAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.project = Project.objects.create(owner=self.user)
        self.section = Section.objects.create(title='test', project=self.project)
        self.task = Task.objects.create(owner=self.user, section=self.section)

    def test_create_task(self):
        response = self.client.post(reverse('task:task_list'),
                                    data={'title': 'test', 'section': self.section.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tasks_list(self):
        response = self.client.get(reverse('task:task_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_task(self):
        response = self.client.put(reverse('task:task', kwargs={'pk': self.task.pk}),
                                   data={'title': 'test2', 'section': self.section.pk, 'position':70})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')
        self.assertEqual(response.data['position'], 70)

    def test_patch_task(self):
        response = self.client.patch(reverse('task:task', kwargs={'pk': self.task.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_put_task_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('task:task', kwargs={'pk': self.task.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_task_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('task:task', kwargs={'pk': self.task.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('task:task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task(self):
        response = self.client.get(reverse('task:task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('task:task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        response = self.client.delete(reverse('task:task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
