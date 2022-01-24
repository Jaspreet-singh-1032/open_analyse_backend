# python imports
import random

# django imports
from django.urls import reverse

# drf imports
from rest_framework.test import APITestCase
from rest_framework import status

# third party imports
from django_seed import Seed

# model imports
from activities.models import (
    ActivityType,
    Activity
)
from user.models import User
from rest_framework.authtoken.models import Token

seeder = Seed.seeder()
faker = Seed.faker()


def turn_on_auto_add_fields(model):
    '''
    When we run seeder.execute()
    seeder set the auto_now=False and auto_now_add=False
    run this function to turn on auto add fields
    '''
    for field in model._meta.fields:
        if hasattr(field, 'auto_now'):
            field.auto_now = True
        if hasattr(field, 'auto_now_add'):
            field.auto_now_add = True


class ActivityTypesApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email=faker.email, password='testuser')
        self.token = Token.objects.create(user=self.user)
        self.list_url = reverse('activity_types-list')

    def create_activity_type(self):
        # used in delete activity type test case
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        data = {
            'name': "test"
        }
        response = self.client.post(self.list_url, data=data)
        return response.json()

    @staticmethod
    def create_activity_type_with_different_user():
        user = User.objects.create(email='new1@gmail.com', password='new')
        activity_type = ActivityType.objects.create(name='test', user=user)
        return activity_type.id

    # ======================= List activity types =======================

    def test_list_activity_types_unauthenticate_fails(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_activity_types_authenticate_succeed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # ======================= Create activity types =======================

    def test_create_activity_type_unauthenticated_fails(self):
        response = self.client.post(self.list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_activity_type_authenticated_empty_data_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(self.list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_activity_type_authenticated_empty_values_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        data = {'name': ""}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_activity_type_authenticated_exceed_max_length_fails(self):
        # max length for activity type name is 100
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        data = {
            'name': "a"*101
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_activity_type_authenticated_valid_data_scceed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        data = {
            'name': "python"
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('name'), data.get('name'))

    def test_create_activity_type_duplicate_name_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        name = faker.name()
        ActivityType.objects.create(name=name, user=self.user)
        data = {
            'name': name
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {
            'detail': ["'{}' for this user already exists!".format(name)]
        }
        )

    # ======================= Delete activity type =======================

    def test_delete_activity_type_invalid_id_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.delete(
            reverse('activity_types-detail', kwargs={'pk': 123123}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_activity_type_valid_id_succeed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        activity = self.create_activity_type()
        response = self.client.delete(
            reverse('activity_types-detail', kwargs={'pk': activity.get('id')}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_activity_type_of_different_user_fails(self):
        # user can only delete data related to him
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        activity_id = self.create_activity_type_with_different_user()
        response = self.client.delete(
            reverse('activity_types-detail', kwargs={'pk': activity_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ======================= Test api actions =======================

    def test_fetch_activities_unauthenticated_fails(self):
        response = self.client.get(
            reverse('activity_types-fetch_activities'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_activities_authenticated_succeed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(
            reverse('activity_types-fetch_activities'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_activities_num_queries(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        seeder.add_entity(ActivityType, 10, {
            'user': self.user
        })
        inserted = seeder.execute()
        seeder.add_entity(Activity, 100, {
            'time_spent': lambda x: random.randint(1, 36000),
            'activity_type': lambda x: ActivityType.objects.get(
                id=random.choice(inserted[ActivityType])
            ),
            'user': self.user
        })
        seeder.execute()
        with self.assertNumQueries(2):
            self.client.get(
                reverse('activity_types-fetch_activities'))

    def test_add_activity_invalid_activity_type_id_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        data = {}
        response = self.client.post(reverse('activity_types-add_activity', kwargs={'pk': 0}), data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_activity_empty_data_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        data = {}
        activity_type = ActivityType.objects.create(name="test", user=self.user)
        response = self.client.post(reverse('activity_types-add_activity', kwargs={'pk': activity_type.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_activity_succeed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        data = {"time_spent": 3600}
        turn_on_auto_add_fields(Activity)
        activity_type = ActivityType.objects.create(name="test1", user=self.user)
        response = self.client.post(reverse('activity_types-add_activity',
                                    kwargs={'pk': activity_type.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivitiesApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email=faker.email(), password=faker.password())
        self.token = Token.objects.create(user=self.user)

    def test_list_activities_unauthenticated_fails(self):
        response = self.client.get(reverse('activities-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_activities_authenticated_succeed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(reverse('activities-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_activities_num_queries(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        activity_type = ActivityType.objects.create(
            user=self.user,
            name=faker.name()
        )
        seeder.add_entity(Activity, 100, {
            'user': self.user,
            'activity_type': activity_type,
            'time_spent': 3600,
        })
        seeder.execute()
        with self.assertNumQueries(2):
            self.client.get(reverse("activities-list"), format="json")
