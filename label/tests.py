from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from label.models import Label
from users.tests import get_user_token


class LabelAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.label = Label.objects.create(owner=self.user, title='test')

    def test_create_label(self):
        response = self.client.post(reverse('label:label_list'), data={'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_labels_list(self):
        response = self.client.get(reverse('label:label_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_label(self):
        response = self.client.put(reverse('label:label', kwargs={'pk': self.label.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_patch_label(self):
        response = self.client.patch(reverse('label:label', kwargs={'pk': self.label.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test2')

    def test_put_label_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('label:label', kwargs={'pk': self.label.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_label_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('label:label', kwargs={'pk': self.label.pk}), data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_label_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('label:label', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_label(self):
        response = self.client.get(reverse('label:label', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_label_not_owner(self):
        user, token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('label:label', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_label(self):
        response = self.client.delete(reverse('label:label', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
