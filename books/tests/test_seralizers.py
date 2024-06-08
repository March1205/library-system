from django.test import TestCase
from books.models import Book
from books.serializers import BookSerializer


class BookSerializerTests(TestCase):

    def setUp(self):
        self.book_data = {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "cover": Book.HARD,
            "inventory": 10,
            "daily_fee": "1.50"
        }
        self.book = Book.objects.create(**self.book_data)

    def test_serialize_book(self):
        """Test serializing a book"""
        serializer = BookSerializer(self.book)
        data = serializer.data

        self.assertEqual(data['id'], self.book.id)
        self.assertEqual(data['title'], self.book.title)
        self.assertEqual(data['author'], self.book.author)
        self.assertEqual(data['cover'], self.book.cover)
        self.assertEqual(data['inventory'], self.book.inventory)
        self.assertEqual(data['daily_fee'], str(self.book.daily_fee))

    def test_deserialize_book(self):
        """Test deserializing data to create a book"""
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()

        self.assertEqual(book.title, self.book_data['title'])
        self.assertEqual(book.author, self.book_data['author'])
        self.assertEqual(book.cover, self.book_data['cover'])
        self.assertEqual(book.inventory, self.book_data['inventory'])
        self.assertEqual(book.daily_fee, float(self.book_data['daily_fee']))

    def test_invalid_deserialize_book(self):
        """Test deserializing invalid data"""
        invalid_data = self.book_data.copy()
        invalid_data['daily_fee'] = 'invalid'

        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('daily_fee', serializer.errors)
