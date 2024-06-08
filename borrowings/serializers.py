from rest_framework import serializers
from books.models import Book
from borrowings.models import Borrowing
from books.serializers import BookSerializer

class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book')

    class Meta:
        model = Borrowing
        fields = "__all__"
