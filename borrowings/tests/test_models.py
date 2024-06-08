from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Book
from borrowings.models import Borrowing
from datetime import date

User = get_user_model()


class BorrowingModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='password123')
        self.book = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover=Book.HARD,
            inventory=10,
            daily_fee="1.50"
        )
        self.borrowing_data = {
            "expected_return_date": date.today(),
            "book": self.book,
            "user": self.user,
        }
        self.borrowing = Borrowing.objects.create(**self.borrowing_data)

    def test_create_borrowing(self):
        """Test creating a borrowing is successful"""
        borrowing = Borrowing.objects.create(**self.borrowing_data)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.expected_return_date, self.borrowing_data["expected_return_date"])
        self.assertIsNone(borrowing.actual_return_date)

    def test_borrowing_str(self):
        """Test the borrowing string representation"""
        self.assertEqual(str(self.borrowing), f"{self.user} borrowed {self.book}")
