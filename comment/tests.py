from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from comment.models import Comment
from project.models import Project
from section.models import Section
from task.models import Task
from users.tests import get_user_token


class CommentAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.project = Project.objects.create(owner=self.user)
        self.section = Section.objects.create(title='test', project=self.project)
        self.task = Task.objects.create(owner=self.user, section=self.section)
        self.comment = Comment.objects.create(owner=self.user, project=self.project, task=self.task)

    def test_create_comment(self):
        response = self.client.post(reverse('comment:comment_list'),
                                    data={'title': 'test', 'project': self.project.pk, 'section': self.section.pk,
                                          'description': 'test description'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comments_list(self):
        response = self.client.get(reverse('comment:comment_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_comment(self):
        response = self.client.put(reverse('comment:comment', kwargs={'pk': self.comment.pk}),
                                   data={'task': self.task.pk, 'project': self.project.pk, 'description': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_comment(self):
        response = self.client.patch(reverse('comment:comment', kwargs={'pk': self.comment.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_comment_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('comment:comment', kwargs={'pk': self.comment.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_comment_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('comment:comment', kwargs={'pk': self.comment.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comment_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('comment:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comment(self):
        response = self.client.get(reverse('comment:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('comment:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment(self):
        response = self.client.delete(reverse('comment:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
