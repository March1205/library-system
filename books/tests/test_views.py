from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from books.models import Book

User = get_user_model()


class BookViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('books:book-list')

        self.book_data = {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "cover": Book.HARD,
            "inventory": 10,
            "daily_fee": "1.50"
        }

        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.admin = User.objects.create_user(email='admin@example.com', password='password', is_staff=True)

        self.book = Book.objects.create(**self.book_data)

        self.user_token = self.get_token(self.user.email, 'password')
        self.admin_token = self.get_token(self.admin.email, 'password')

    def get_token(self, email, password):
        response = self.client.post(reverse('users:login'), {'email': email, 'password': password}, format='json')
        return response.data['access']

    def test_list_books(self):
        """Test that any user can list books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book_non_admin(self):
        """Test that non-admin users cannot create a book"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        response = self.client.post(self.list_url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_admin(self):
        """Test that admin users can create a book"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.admin_token)
        response = self.client.post(self.list_url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_non_admin(self):
        """Test that non-admin users cannot update a book"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        update_url = reverse('books:book-detail', args=[self.book.id])
        response = self.client.put(update_url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_admin(self):
        """Test that admin users can update a book"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.admin_token)
        update_url = reverse('books:book-detail', args=[self.book.id])
        response = self.client.put(update_url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_non_admin(self):
        """Test that non-admin users cannot delete a book"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        delete_url = reverse('books:book-detail', args=[self.book.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_admin(self):
        """Test that admin users can delete a book"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.admin_token)
        delete_url = reverse('books:book-detail', args=[self.book.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
