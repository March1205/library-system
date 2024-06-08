from rest_framework import viewsets
from borrowings.serializers import BorrowingSerializer
from borrowings.models import Borrowing
from rest_framework.permissions import IsAuthenticated


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
