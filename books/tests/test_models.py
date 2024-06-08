from django.test import TestCase
from books.models import Book


class BookModelTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover=Book.HARD,
            inventory=10,
            daily_fee=1.50
        )

    def test_create_book(self):
        """Test creating a book is successful"""
        self.assertEqual(self.book.title, "The Great Gatsby")
        self.assertEqual(self.book.author, "F. Scott Fitzgerald")
        self.assertEqual(self.book.cover, Book.HARD)
        self.assertEqual(self.book.inventory, 10)
        self.assertEqual(self.book.daily_fee, 1.50)

    def test_book_str(self):
        """Test the book string representation"""
        expected_str = f"{self.book.id} - {self.book.title}"
        self.assertEqual(str(self.book), expected_str)

    def test_book_cover_choices(self):
        """Test the cover choices are correct"""
        self.assertIn(self.book.cover, [choice[0] for choice in Book.COVER_CHOICES])
