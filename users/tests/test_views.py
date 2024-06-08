from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewsTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:create')
        self.token_url = reverse('users:login')
        self.me_url = reverse('users:manage')

        self.user_data = {
            "email": "user@example.com",
            "password": "password123",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user_token = self.get_token(self.user.email, self.user_data['password'])

        self.admin_data = {
            "email": "admin@example.com",
            "password": "password123",
            "is_staff": True,
        }
        self.admin = User.objects.create_user(**self.admin_data)
        self.admin_token = self.get_token(self.admin.email, self.admin_data['password'])

    def get_token(self, email, password):
        response = self.client.post(self.token_url, {'email': email, 'password': password}, format='json')
        return response.data['access']

    def test_register_user(self):
        """Test user registration"""
        user_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data)
        self.assertNotIn('password', response.data)

    def test_create_token(self):
        """Test creating a token for the user"""
        response = self.client.post(self.token_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_retrieve_user_profile(self):
        """Test retrieving user profile for logged in user"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_profile(self):
        """Test updating the user profile for logged in user"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        update_data = {
            "email": "updateduser@example.com",
            "password": "newpassword123",
        }
        response = self.client.put(self.me_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, update_data['email'])
        self.assertTrue(self.user.check_password(update_data['password']))
