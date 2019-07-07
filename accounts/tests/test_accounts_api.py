from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('accounts:signup')
LOGIN_USER_URL = reverse('accounts:login')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class RegisterViewTest(TestCase):
    """
    Test the Register API
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self):
        """
        Test creating user with a valid payload is successful
        """

        payload = {
            "username": "test",
            "email": "test@example.com",
            "password": "testpass",
            "confirm_password": "testpass"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn("password", res.data)

    def test_create_user_with_invalid_payload(self):
        """
        Test user creation with invalid payload
        """
        payload = {
            "username": "test",
            "email": "test@example.com",
            "password": "testpass",
            "confirm_password": "pass"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(TestCase):
    """
    Test JWT user authentication
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_user_success(self):
        """
        Test user JWT login
        """
        user_creation_payload = {
            "username": "test",
            "email": "test@example.com",
            "password": "testpass"
        }
        create_user(**user_creation_payload)

        payload = {
            "username": "test",
            "password": "testpass"

        }
        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_payload(self):
        user_creation_payload = {
            "username": "test",
            "email": "test@example.com",
            "password": "testpass"
        }
        create_user(**user_creation_payload)

        payload = {
            "username": "",
            "password": "testpass"
        }
        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)
