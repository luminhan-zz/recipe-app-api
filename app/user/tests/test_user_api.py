from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


def create_user(**params):
    return get_user_model().objects.create_user(**params)

ME_URL = reverse('user:me')


class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name': self.user.name,
                                    'email': self.user.email})

    def test_post_not_allowed(self):
        """Test that POST is not allowed on me url"""

        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'newname',
                   'password': 'newpassword'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(payload['name'], self.user.name)
        self.assertTrue(self.user.check_password(payload['password']))


