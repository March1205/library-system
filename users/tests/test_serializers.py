from django.test import TestCase
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializerTests(TestCase):

    def setUp(self):
        self.user_data = {
            "email": "user@example.com",
            "password": "password123",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.serializer = UserSerializer(instance=self.user)

    def test_serialize_user(self):
        """Test serializing a user"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.user.id)
        self.assertEqual(data['email'], self.user.email)
        self.assertNotIn('password', data)
        self.assertEqual(data['is_staff'], self.user.is_staff)

    def test_deserialize_user(self):
        """Test deserializing data to create a user"""
        user_data = {
            "email": "newuser@example.com",
            "password": "password123",
        }
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertEqual(user.email, user_data['email'])
        self.assertTrue(user.check_password(user_data['password']))
        self.assertFalse(user.is_staff)

    def test_update_user(self):
        """Test updating a user"""
        update_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        serializer = UserSerializer(instance=self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, update_data['email'])
        self.assertTrue(user.check_password(update_data['password']))


class AuthTokenSerializerTests(TestCase):

    def setUp(self):
        self.user_data = {
            "email": "user@example.com",
            "password": "password123",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token_data = {
            "email": self.user.email,
            "password": self.user_data['password'],
        }

    def test_auth_token_serializer(self):
        """Test the AuthTokenSerializer"""
        serializer = AuthTokenSerializer(data=self.token_data)
        self.assertTrue(serializer.is_valid())
        data = serializer.validated_data

        self.assertIn('access', data)
        self.assertIn('refresh', data)
        self.assertEqual(data['email'], self.user.email)
