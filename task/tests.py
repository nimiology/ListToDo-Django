from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from task.models import Project, ProjectUser, Label, Section, Task, Comment
from users.tests import get_user_token


class ProjectAPITestCase(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.project = Project.objects.create(owner=self.user)

    def test_create_project(self):
        response = self.client.post(reverse('tasks:projects_list'), data={'title': 'test', })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_projects_list(self):
        response = self.client.get(reverse('tasks:projects_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project(self):
        response = self.client.get(reverse('tasks:project', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:project', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_project(self):
        response = self.client.delete(reverse('tasks:project', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('tasks:project', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_project(self):
        response = self.client.put(reverse('tasks:project', kwargs={'pk': self.project.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_put_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('tasks:project', kwargs={'pk': self.project.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_project(self):
        response = self.client.patch(reverse('tasks:project', kwargs={'pk': self.project.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_patch_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('tasks:project', kwargs={'pk': self.project.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_project_invite_slug(self):
        response = self.client.get(reverse('tasks:change_invite_slug', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_project_invite_slug_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:change_invite_slug', kwargs={'pk': self.project.pk}), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_join_to_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:join_to_project', kwargs={'invite_slug': self.project.invite_slug}), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:leave_project', kwargs={
            'pk': ProjectUser.objects.create(owner=user, project=self.project).project.pk}), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_project_not_in_project(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:leave_project', kwargs={
            'pk': self.project.pk}), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_personalize_project_put(self):
        response = self.client.put(reverse('tasks:personalize_project', kwargs={'pk': self.project.pk}),
                                   data={'color': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_personalize_project_patch(self):
        response = self.client.patch(reverse('tasks:personalize_project', kwargs={'pk': self.project.pk}),
                                     data={'color': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_personalize_project_put_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('tasks:personalize_project', kwargs={'pk': self.project.pk}),
                                   data={'color': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_personalize_project_patch_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('tasks:personalize_project', kwargs={'pk': self.project.pk}),
                                     data={'color': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LabelAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.label = Label.objects.create(owner=self.user, title='test')

    def test_create_label(self):
        response = self.client.post(reverse('tasks:label_list'), data={'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_labels_list(self):
        response = self.client.get(reverse('tasks:label_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_label(self):
        response = self.client.put(reverse('tasks:label', kwargs={'pk': self.label.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_patch_label(self):
        response = self.client.patch(reverse('tasks:label', kwargs={'pk': self.label.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_put_label_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('tasks:label', kwargs={'pk': self.label.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_label_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('tasks:label', kwargs={'pk': self.label.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_label_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:label', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_label(self):
        response = self.client.get(reverse('tasks:label', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_label_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('tasks:label', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_label(self):
        response = self.client.delete(reverse('tasks:label', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SectionAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.project = Project.objects.create(owner=self.user)
        self.section = Section.objects.create(title='test', project=self.project)

    def test_create_section(self):
        response = self.client.post(reverse('tasks:section_list'),
                                    data={'title': 'test', 'project': self.project.pk, 'position': 102})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_sections_list(self):
        response = self.client.get(reverse('tasks:section_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_section(self):
        response = self.client.put(reverse('tasks:section', kwargs={'pk': self.section.pk}),
                                   data={'title': 'test2', 'project': self.project.pk, 'position': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_patch_section(self):
        response = self.client.patch(reverse('tasks:section', kwargs={'pk': self.section.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_put_section_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('tasks:section', kwargs={'pk': self.section.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_section_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('tasks:section', kwargs={'pk': self.section.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_section_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:section', kwargs={'pk': self.section.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_section(self):
        response = self.client.get(reverse('tasks:section', kwargs={'pk': self.section.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_section_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('tasks:section', kwargs={'pk': self.section.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_section(self):
        response = self.client.delete(reverse('tasks:section', kwargs={'pk': self.section.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.project = Project.objects.create(owner=self.user)
        self.section = Section.objects.create(title='test', project=self.project)
        self.task = Task.objects.create(owner=self.user, section=self.section)
        self.comment = Comment.objects.create(owner=self.user, project=self.project, task=self.task)

    def test_create_comment(self):
        response = self.client.post(reverse('tasks:comment_list'),
                                    data={'title': 'test', 'project': self.project.pk, 'section': self.section.pk,
                                          'description': 'test description'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comments_list(self):
        response = self.client.get(reverse('tasks:comment_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_comment(self):
        response = self.client.put(reverse('tasks:comment', kwargs={'pk': self.comment.pk}),
                                   data={'task': self.task.pk, 'project': self.project.pk, 'description': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_comment(self):
        response = self.client.patch(reverse('tasks:comment', kwargs={'pk': self.comment.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_comment_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('tasks:comment', kwargs={'pk': self.comment.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_comment_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('tasks:comment', kwargs={'pk': self.comment.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comment_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comment(self):
        response = self.client.get(reverse('tasks:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('tasks:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment(self):
        response = self.client.delete(reverse('tasks:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TaskAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.project = Project.objects.create(owner=self.user)
        self.section = Section.objects.create(title='test', project=self.project)
        self.task = Task.objects.create(owner=self.user, section=self.section)

    def test_create_task(self):
        response = self.client.post(reverse('tasks:task_list'),
                                    data={'title': 'test', 'section': self.section.pk, 'position': 102})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tasks_list(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_task(self):
        response = self.client.put(reverse('tasks:task', kwargs={'pk': self.task.pk}),
                                   data={'title': 'test2', 'section': self.section.pk, 'position': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_patch_task(self):
        response = self.client.patch(reverse('tasks:task', kwargs={'pk': self.task.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_put_task_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('tasks:task', kwargs={'pk': self.task.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_task_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('tasks:task', kwargs={'pk': self.task.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks:task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task(self):
        response = self.client.get(reverse('tasks:task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('tasks:task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        response = self.client.delete(reverse('tasks:task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ActivityAPITestCase(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_get_activity_list(self):
        response = self.client.get(reverse('tasks:activity'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

