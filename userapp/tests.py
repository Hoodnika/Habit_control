from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from userapp.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(tg_username='test')
        self.user.set_password('12345')
        self.user.save()
        self.another_user = User.objects.create(tg_username='another_test')
        # self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        url = reverse('userapp:register')
        data = {
            'tg_username': 'test_user_2',
            'password': 'test_password',
        }
        response = self.client.post(url, data)  # как анонимный пользователь
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        url = reverse('userapp:register')
        data_1 = {
            'tg_username': 'test_user_2',
        }
        response_1 = self.client.post(url, data_1)  # как анонимный пользователь
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        data_2 = {
            'tg_username': 'test',
            'password': 'test_pass',
        }
        response_2 = self.client.post(url, data_2)  # как анонимный пользователь
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        url = reverse('userapp:login')
        data = {
            'tg_username': 'test',
            'password': '12345',
        }
        response = self.client.post(url, data)  # как анонимный пользователь
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        url = reverse('userapp:login')
        data = {
            'tg_username': 'test',
            'password': '1234',
        }
        response = self.client.post(url, data)  # как анонимный пользователь
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_users(self):
        url = reverse('userapp:user_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user(self):
        url = reverse('userapp:user_get', args={self.user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('tg_username'), 'test')

    def test_retrieve_unauthorized_user(self):
        url = reverse('userapp:user_get', args={self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_another_retrieve_user(self):
        url = reverse('userapp:user_get', args={self.another_user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user(self):
        url = reverse('userapp:user_update', args={self.user.pk})
        self.client.force_authenticate(user=self.user)
        data = {
            'tg_username': 'edit_test_user',
            'first_name': 'jojo'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('tg_username'), 'edit_test_user')
        self.assertEqual(data.get('first_name'), 'jojo')

    def test_another_update_user(self):
        url = reverse('userapp:user_update', args={self.another_user.pk})
        self.client.force_authenticate(user=self.user)
        data = {
            'tg_username': 'edit_test_user',
            'first_name': 'jojo'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_unauthorized_user(self):
        url = reverse('userapp:user_update', args={self.another_user.pk})
        data = {
            'tg_username': 'edit_test_user',
            'first_name': 'jojo'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        url = reverse('userapp:user_delete', args={self.user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_another_delete_user(self):
        url = reverse('userapp:user_delete', args={self.another_user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_unauthorized_user(self):
        url = reverse('userapp:user_delete', args={self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
