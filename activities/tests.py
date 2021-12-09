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

seeder = Seed()
faker = seeder.faker()

class ActivityTypesApiTestCase(APITestCase):
    def setUp(self):
        data = {
            'email': "test@gmail.com",
            'password': 'test'
        }
        self.user = User.objects.create(
            email='testuser@gmail.com', password='testuser')
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
        user = User.objects.create(email='new@gmail.com', password='new')
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
        ActivityType.objects.create(name = name , user = self.user)
        data = {
            'name':name
        }
        response = self.client.post(self.list_url , data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), 
            {
                'detail':["'{}' for this user already exists!".format(name)]
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
