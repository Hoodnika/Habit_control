from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mainapp.models import Place, Habit
from userapp.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(tg_username='test')
        self.another_user = User.objects.create(tg_username='another_test')
        self.client.force_authenticate(user=self.user)
        self.place = Place.objects.create(place_name='test_place_name', user=self.user)
        self.another_place = Place.objects.create(place_name='test_another_place_name', user=self.another_user)
        self.related_habit_nice = Habit.objects.create(
            user=self.user,
            habit_name='test_related_nice_habit_name',
            time_to_action="08:00:00",
            periodicity=Habit.Periodicity.per_day,
            is_nice=True,
            time_to_complete=timedelta(60),
        )
        self.related_habit_not_nice = Habit.objects.create(
            user=self.user,
            habit_name='test_related_not_nice_habit_name',
            time_to_action="08:00:00",
            periodicity=Habit.Periodicity.per_day,
            is_nice=False,
            time_to_complete=timedelta(60),
        )
        self.another_habit = Habit.objects.create(
            user=self.another_user,
            habit_name='test_another_habit_name',
            time_to_action="08:00:00",
            periodicity=Habit.Periodicity.per_day,
            is_nice=True,
            is_public=True,
            time_to_complete=timedelta(60),
        )

    def test_create_habit(self):
        url = reverse('mainapp:habit_create')
        data = {
            'user': self.user.pk,
            'place': self.place.pk,
            'habit_name': 'test_habit_name',
            'time_to_action': "08:00:00",
            'periodicity': Habit.Periodicity.per_day,
            'reward': 'test_reward',
            'time_to_complete': 60,

        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('habit_name'), 'test_habit_name')
        self.assertEqual(data.get('periodicity'), 'раз в день')
        self.assertEqual(data.get('is_public'), False)
        self.assertEqual(data.get('is_nice'), False)

    def test_create_with_related_and_reward(self):
        url = reverse('mainapp:habit_create')
        data = {
            'user': self.user.pk,
            'place': self.place.pk,
            'related_habit': self.related_habit_nice.pk,
            'habit_name': 'test_habit_name',
            'time_to_action': "08:00:00",
            'periodicity': Habit.Periodicity.per_day,
            'reward': 'test_reward',
            'time_to_complete': 60,
        }
        response = self.client.post(url, data)
        self.assertIn('Укажите или связанную привычку или вознаграждение', response.content.decode('utf-8'))

    def test_create_with_nice_and_reward(self):
        url = reverse('mainapp:habit_create')
        data = {
            'user': self.user.pk,
            'place': self.place.pk,
            'habit_name': 'test_habit_name',
            'time_to_action': "08:00:00",
            'periodicity': Habit.Periodicity.per_day,
            'reward': 'test_reward',
            'is_nice': True,
            'time_to_complete': 60,
        }
        response = self.client.post(url, data)
        self.assertIn('У приятной привычки не может быть вознаграждения', response.content.decode('utf-8'))

    def test_create_with_nice_and_related(self):
        url = reverse('mainapp:habit_create')
        data = {
            'user': self.user.pk,
            'place': self.place.pk,
            'related_habit': self.related_habit_nice.pk,
            'habit_name': 'test_habit_name',
            'time_to_action': "08:00:00",
            'periodicity': Habit.Periodicity.per_day,
            'is_nice': True,
            'time_to_complete': 60,
        }
        response = self.client.post(url, data)
        self.assertIn('У приятной привычки не может быть связанной привычки', response.content.decode('utf-8'))

    def test_create_with_not_nice_related(self):
        url = reverse('mainapp:habit_create')
        data = {
            'user': self.user.pk,
            'place': self.place.pk,
            'related_habit': self.related_habit_not_nice.pk,
            'habit_name': 'test_habit_name',
            'time_to_action': "08:00:00",
            'periodicity': Habit.Periodicity.per_day,
            'is_nice': True,
            'time_to_complete': 60,
        }
        response = self.client.post(url, data)
        self.assertIn('У связанной привычки должен быть признак приятной.', response.content.decode('utf-8'))

    def test_create_with_invalid_periodicity(self):
        url = reverse('mainapp:habit_create')
        data = {
            'user': self.user.pk,
            'place': self.place.pk,
            'habit_name': 'test_habit_name',
            'time_to_action': "08:00:00",
            'periodicity': 'раз в меясц',
            'is_nice': True,
            'time_to_complete': 60,
        }
        response = self.client.post(url, data)
        self.assertIn('Значения раз в меясц нет среди допустимых вариантов.', response.content.decode('utf-8'))

    def test_create_with_invalid_time_to_complete(self):
        url = reverse('mainapp:habit_create')
        data = {
            'user': self.user.pk,
            'place': self.place.pk,
            'habit_name': 'test_habit_name',
            'time_to_action': "08:00:00",
            'periodicity': Habit.Periodicity.per_day,
            'is_nice': True,
            'time_to_complete': 121,
        }
        response = self.client.post(url, data)
        self.assertIn('Убедитесь, что это значение меньше либо равно 0:02:00.', response.content.decode('utf-8'))

    def test_HabitListAPIView(self):
        url = reverse('mainapp:habit_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['results'][0]['habit_name'], 'test_another_habit_name')
        self.assertEqual(data['results'][0]['is_public'], True)
        self.assertEqual(data['results'][0]['user'], 4)

    def test_HabitPersonalListAPIView(self):
        url = reverse('mainapp:habit_personal_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['results'][0]['user'], 5)
        self.assertEqual(data['results'][1]['user'], 5)

    def test_HabitRetrieveAPIView(self):
        url = reverse('mainapp:habit_get', args={self.related_habit_nice.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['habit_name'], 'test_related_nice_habit_name')

    def test_another_HabitRetrieveAPIView(self):
        url = reverse('mainapp:habit_get', args={self.another_habit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_HabitUpdateAPIView(self):
        url = reverse('mainapp:habit_update', args={self.related_habit_not_nice.pk})
        data = {
            'habit_name': 'edit_test_habit_name_edit'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['habit_name'], 'edit_test_habit_name_edit')

    def test_another_HabitUpdateAPIView(self):
        url = reverse('mainapp:habit_update', args={self.another_habit.pk})
        data = {
            'habit_name': 'edit_test_habit_name_edit'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_HabitDestroyAPIView(self):
        url = reverse('mainapp:habit_delete', args={self.related_habit_nice.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_another_HabitDestroyAPIView(self):
        url = reverse('mainapp:habit_delete', args={self.another_habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PlaceTestcase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(tg_username='test_user')
        self.another_user = User.objects.create(tg_username='another_test')
        self.client.force_authenticate(user=self.user)
        self.place = Place.objects.create(place_name='test_place', user=self.user)
        self.another_place = Place.objects.create(place_name='another_test_place', user=self.another_user)

    def test_create_place(self):
        url = reverse('mainapp:place-list')
        data = {
            'place_name': 'test_place_name_test',
            'address': 'test_address',
            'user': self.user.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['place_name'], 'test_place_name_test')
        self.assertEqual(data['address'], 'test_address')

    def test_list_place(self):
        url = reverse('mainapp:place-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['results'][0]['place_name'], 'test_place')

    def test_retrieve_place(self):
        url = reverse('mainapp:place-detail', args={self.place.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['place_name'], 'test_place')

    def test_another_retrieve_place(self):
        url = reverse('mainapp:place-detail', args={self.another_place.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # 404 потому что в views.py place.queryset = Place.objects.filter(user=self.request.user)

    def test_update_place(self):
        url = reverse('mainapp:place-detail', args={self.place.pk})
        data = {
            'place_name': 'edit_test_place_name_edit',
            'address': 'edit_test_address',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('place_name'), 'edit_test_place_name_edit')

    def test_another_update_place(self):
        url = reverse('mainapp:place-detail', args={self.another_place.pk})
        data = {
            'place_name': 'edit_test_place_name_edit',
            'address': 'edit_test_address',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # 404 потому что в views.py place.queryset = Place.objects.filter(user=self.request.user)

    def test_delete_place(self):
        url = reverse('mainapp:place-detail', args={self.place.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_another_delete_place(self):
        url = reverse('mainapp:place-detail', args={self.another_place.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # 404 потому что в views.py place.queryset = Place.objects.filter(user=self.request.user)
