from rest_framework import viewsets, status
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer
)
from borrowings.models import Borrowing
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone


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

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            return Response(
                {"error": "Book already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = timezone.now()
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        return Response(
            {"status": "Book returned successfully"},
            status=status.HTTP_200_OK
        )
