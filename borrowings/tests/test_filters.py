from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from books.models import Book
from borrowings.models import Borrowing
from borrowings.filters import BorrowingFilter
from datetime import date, timedelta

User = get_user_model()


class BorrowingFilterTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='user@example.com', password='password123')
        self.admin = User.objects.create_user(email='admin@example.com', password='password123', is_staff=True)
        self.book = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover=Book.HARD,
            inventory=10,
            daily_fee="1.50"
        )
        self.borrowing1 = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            book=self.book,
            user=self.user
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            actual_return_date=date.today(),
            book=self.book,
            user=self.user
        )

    def test_filter_is_active(self):
        """Test filtering borrowings by is_active parameter"""
        request = self.factory.get('/borrowings/', {'is_active': 'true'})
        request.user = self.user
        filtered_borrowings = BorrowingFilter(request.GET, queryset=Borrowing.objects.all(), request=request).qs
        self.assertIn(self.borrowing1, filtered_borrowings)
        self.assertNotIn(self.borrowing2, filtered_borrowings)

    def test_filter_user_id_admin(self):
        """Test filtering borrowings by user_id for admin users"""
        request = self.factory.get('/borrowings/', {'user_id': self.user.id})
        request.user = self.admin
        filtered_borrowings = BorrowingFilter(request.GET, queryset=Borrowing.objects.all(), request=request).qs
        self.assertIn(self.borrowing1, filtered_borrowings)
        self.assertIn(self.borrowing2, filtered_borrowings)

    def test_filter_user_id_non_admin(self):
        """Test that non-admin users cannot filter by user_id"""
        request = self.factory.get('/borrowings/', {'user_id': self.user.id})
        request.user = self.user
        filtered_borrowings = BorrowingFilter(request.GET, queryset=Borrowing.objects.all(), request=request).qs
        self.assertNotIn('user_id', BorrowingFilter(request.GET, queryset=Borrowing.objects.all(), request=request).filters)
        self.assertIn(self.borrowing1, filtered_borrowings)
        self.assertIn(self.borrowing2, filtered_borrowings)
