# django imports
from django.test import TestCase
from django.urls import reverse

# drf imports
from rest_framework import status

# modal imports
from user.models import User


class UserAPITestCase(TestCase):

    def setUp(self):
        user = User(email='test@gmail.com')
        user.set_password('test')
        user.save()

    # ======================= Login Test Cases =======================

    def test_user_login_empty_data_fails(self):
        data = {}
        response = self.client.post(reverse('user-login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_empty_values_fails(self):
        data = {
            "email": "",
            "password": ""
        }
        response = self.client.post(reverse('user-login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_invalid_credentials_fails(self):
        data = {
            'email': "random@gmail.com",
            "password": "random"
        }
        response = self.client.post(reverse('user-login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_invalid_email_fails(self):
        data = {
            'email': "random@gmail.com",
            "password": "test"
        }
        response = self.client.post(reverse('user-login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_invalid_password_fails(self):
        data = {
            'email': "test@gmail.com",
            "password": "random"
        }
        response = self.client.post(reverse('user-login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_correct_credentials_succeed(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'test'
        }
        response = self.client.post(reverse('user-login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ========================================================================

    # ======================= User Register Test Cases =======================
    def test_user_register_empty_data_fails(self):
        data = {}
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_email_already_exists_fails(self):
        data = {
            'email': "test@gmail.com",
            "password": "test123"
        }
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_empty_values_fails(self):
        data = {
            'email': '',
            'password': ''
        }
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_empty_email_fails(self):
        data = {
            'email': '',
            'password': '123'
        }
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_empty_password_fails(self):
        data = {
            'email': 'new@gmail.com',
            'password': ''
        }
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_invalid_email_fails(self):
        data = {
            'email': 'test.com',
            'password': 'test'
        }
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_succeed(self):
        data = {
            'email': 'new@gmail.com',
            'password': 'new'
        }
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ===========================================================================
