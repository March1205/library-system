import django_filters
from borrowings.models import Borrowing


class BorrowingFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(
        field_name='actual_return_date',
        lookup_expr='isnull',
        label='Is Active'
    )
    user_id = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Borrowing
        fields = ('is_active', 'user_id')

    def __init__(self, *args, **kwargs):
        super(BorrowingFilter, self).__init__(*args, **kwargs)
        user = kwargs['request'].user
        if not user.is_staff:
            del self.filters['user_id']
