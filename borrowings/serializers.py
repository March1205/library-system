from rest_framework import serializers
from django.utils import timezone
from books.models import Book
from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    borrow_date = serializers.DateField(read_only=True)
    expected_return_date = serializers.DateField()
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "book", "book_id", "user")

    def validate_expected_return_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Expected return date must be after the current date.")
        return value


class BorrowingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    borrow_date = serializers.DateField(read_only=True)
    expected_return_date = serializers.DateField()
    actual_return_date = serializers.DateField(
        required=False, allow_null=True
    )
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book'
    )
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "book_id",
            "user_id"
        )

    def validate_expected_return_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError(
                "Expected return date must be after the current date."
            )
        return value
