import hashlib

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.seeds.models import UserFactory


class SignInAPITestCase(APITestCase):
    def setUp(self):
        self.super_secret_password = hashlib.sha256().hexdigest()
        self.user = UserFactory(password=self.super_secret_password)

    def test_signin_post_success(self):
        url = reverse('signin')
        payload = {
            'username': self.user.username,
            'password': self.super_secret_password,
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.data.get('status'), 'success')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_post_fail_non_username_informed(self):
        url = reverse('signin')
        payload = {
            'username': '',
            'password': self.super_secret_password,
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.data.get('status'), 'fail')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_post_fail_non_password_informed(self):
        url = reverse('signin')
        payload = {
            'username': self.user.username,
            'password': '',
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.data.get('status'), 'fail')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_post_fail_wrong_password(self):
        url = reverse('signin')
        payload = {
            'username': self.user.username,
            'password': hashlib.blake2b(digest_size=10).hexdigest(),
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.data.get('status'), 'fail')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
