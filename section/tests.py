from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project.models import Project
from section.models import Section
from users.tests import get_user_token


class SectionAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.project = Project.objects.create(owner=self.user)
        self.section = Section.objects.create(title='test', project=self.project)

    def test_create_section(self):
        response = self.client.post(reverse('section:section_list'),
                                    data={'title': 'test', 'project': self.project.pk, 'position': 102})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_sections_list(self):
        response = self.client.get(reverse('section:section_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_section(self):
        response = self.client.put(reverse('section:section', kwargs={'pk': self.section.pk}),
                                   data={'title': 'test2', 'project': self.project.pk, 'position': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_patch_section(self):
        response = self.client.patch(reverse('section:section', kwargs={'pk': self.section.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_put_section_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('section:section', kwargs={'pk': self.section.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_section_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('section:section', kwargs={'pk': self.section.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_section_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('section:section', kwargs={'pk': self.section.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_section(self):
        response = self.client.get(reverse('section:section', kwargs={'pk': self.section.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_section_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('section:section', kwargs={'pk': self.section.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_section(self):
        response = self.client.delete(reverse('section:section', kwargs={'pk': self.section.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


