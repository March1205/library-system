from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from books.models import Book
from borrowings.models import Borrowing
from datetime import date, timedelta

User = get_user_model()


class BorrowingViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.borrowing_list_url = reverse('borrowings:borrowing-list')
        self.book = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover=Book.HARD,
            inventory=10,
            daily_fee="1.50"
        )
        self.user = User.objects.create_user(email='user@example.com', password='password123')
        self.admin = User.objects.create_user(email='admin@example.com', password='password123', is_staff=True)

        self.user_token = self.get_token(self.user.email, 'password123')
        self.admin_token = self.get_token(self.admin.email, 'password123')

        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            book=self.book,
            user=self.user
        )

    def get_token(self, email, password):
        response = self.client.post(reverse('users:login'), {'email': email, 'password': password}, format='json')
        return response.data['access']

    def test_create_borrowing(self):
        """Test creating a new borrowing"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        borrowing_data = {
            "expected_return_date": date.today() + timedelta(days=7),
            "book_id": self.book.id,
        }
        response = self.client.post(self.borrowing_list_url, borrowing_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 2)

    def test_filter_borrowings_by_user_id_admin(self):
        """Test filtering borrowings by user_id for admin users"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.admin_token)
        response = self.client.get(self.borrowing_list_url, {'user_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_borrowings_by_is_active(self):
        """Test filtering borrowings by is_active parameter"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        response = self.client.get(self.borrowing_list_url, {'is_active': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_return_book(self):
        """Test returning a book"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        return_url = reverse('borrowings:borrowing-return-book', args=[self.borrowing.id])
        response = self.client.post(return_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.borrowing.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)

    def test_return_book_twice(self):
        """Test that a book cannot be returned twice"""
        self.client.credentials(HTTP_AUTHORIZE='Authorize ' + self.user_token)
        return_url = reverse('borrowings:borrowing-return-book', args=[self.borrowing.id])
        self.client.post(return_url)
        response = self.client.post(return_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
