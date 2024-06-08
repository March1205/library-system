from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from borrowings.serializers import BorrowingCreateSerializer, BorrowingSerializer
from books.models import Book
from borrowings.models import Borrowing
from datetime import date, timedelta

User = get_user_model()


class BorrowingSerializerTests(TestCase):

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
            "expected_return_date": date.today() + timedelta(days=7),
            "book": self.book,
            "user": self.user,
        }
        self.borrowing = Borrowing.objects.create(**self.borrowing_data)
        self.factory = APIRequestFactory()

    def test_serialize_borrowing(self):
        """Test serializing a borrowing"""
        serializer = BorrowingSerializer(instance=self.borrowing)
        data = serializer.data

        self.assertEqual(data['id'], self.borrowing.id)
        self.assertEqual(data['borrow_date'], str(self.borrowing.borrow_date))
        self.assertEqual(data['expected_return_date'], str(self.borrowing.expected_return_date))
        self.assertEqual(data['actual_return_date'], self.borrowing.actual_return_date)
        self.assertEqual(data['book']['id'], self.book.id)
        self.assertEqual(data['book_id'], self.book.id)
        self.assertEqual(data['user_id'], self.user.id)

    def test_deserialize_borrowing_create(self):
        """Test deserializing data to create a borrowing"""
        borrowing_data = {
            "expected_return_date": date.today() + timedelta(days=7),
            "book_id": self.book.id,
        }
        request = self.factory.post('/api/borrowings/', borrowing_data)
        request.user = self.user

        serializer = BorrowingCreateSerializer(data=borrowing_data, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        borrowing = serializer.save()

        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.expected_return_date, borrowing_data["expected_return_date"])
        self.assertIsNone(borrowing.actual_return_date)

    def test_validate_expected_return_date(self):
        """Test validating expected return date"""
        invalid_data = {
            "expected_return_date": date.today() - timedelta(days=1),
            "book_id": self.book.id,
        }
        request = self.factory.post('/api/borrowings/', invalid_data)
        request.user = self.user

        serializer = BorrowingCreateSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('expected_return_date', serializer.errors)
        self.assertEqual(str(serializer.errors['expected_return_date'][0]), "Expected return date must be after the current date.")
