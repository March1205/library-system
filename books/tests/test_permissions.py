from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS
from books.permissions import IsAdminOrReadOnly

User = get_user_model()


class IsAdminOrReadOnlyTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='user@example.com', password='password')
        self.admin = User.objects.create_user(
            email='admin@example.com', password='password', is_staff=True)
        self.permission = IsAdminOrReadOnly()

    def test_safe_methods(self):
        """Test that safe methods are allowed for any user"""
        for method in SAFE_METHODS:
            request = self.factory.get('/')
            request.method = method
            request.user = self.user
            self.assertTrue(self.permission.has_permission(request, None))

    def test_unsafe_methods_non_admin(self):
        """Test that unsafe methods are not allowed for non-admin users"""
        for method in ['POST', 'PUT', 'DELETE']:
            request = self.factory.post('/')
            request.method = method
            request.user = self.user
            self.assertFalse(self.permission.has_permission(request, None))

    def test_unsafe_methods_admin(self):
        """Test that unsafe methods are allowed for admin users"""
        for method in ['POST', 'PUT', 'DELETE']:
            request = self.factory.post('/')
            request.method = method
            request.user = self.admin
            self.assertTrue(self.permission.has_permission(request, None))
