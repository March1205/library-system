from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):

    def setUp(self):
        self.user_data = {
            "email": "user@example.com",
            "password": "password123",
        }
        self.superuser_data = {
            "email": "admin@example.com",
            "password": "password123",
        }

    def test_create_user(self):
        """Test creating a regular user is successful"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser is successful"""
        superuser = User.objects.create_superuser(**self.superuser_data)
        self.assertEqual(superuser.email, self.superuser_data["email"])
        self.assertTrue(superuser.check_password(self.superuser_data["password"]))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_email_normalization(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(email, 'password123')
        self.assertEqual(user.email, email.lower())

    def test_create_user_without_email(self):
        """Test creating a user without an email raises an error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'password123')

    def test_create_superuser_without_is_staff(self):
        """Test creating a superuser without is_staff=True raises an error"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='admin@example.com', password='password123', is_staff=False)

    def test_create_superuser_without_is_superuser(self):
        """Test creating a superuser without is_superuser=True raises an error"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='admin@example.com', password='password123', is_superuser=False)
