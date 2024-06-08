from rest_framework import viewsets
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer
)
from borrowings.models import Borrowing
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.inventory > 0:
            book.inventory -= 1
            book.save()
            serializer.save(user=self.request.user)
        else:
            raise ValidationError("Book is out of stock")

    def perform_update(self, serializer):
        instance = self.get_object()
        if "actual_return_date" in serializer.validated_data and not instance.actual_return_date:
            book = instance.book
            book.inventory += 1
            book.save()
        serializer.save()
