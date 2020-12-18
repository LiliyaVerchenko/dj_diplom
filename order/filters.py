from django_filters import rest_framework as filters
from order.models import Order
from product.models import Product

CHOICES_STATUS = (
        ('NEW', 'Новый заказ'),
        ('IN_PROGRESS', 'В обработке'),
        ('DONE', 'Выполнен')
    )

class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(
        choices=CHOICES_STATUS
    )
    amount_less = filters.NumberFilter(
        field_name='order_amount',
        lookup_expr='lte'
    )
    amount_greater = filters.NumberFilter(
        field_name='order_amount',
        lookup_expr='gte'
    )
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    positions = filters.ModelChoiceFilter(
        field_name="position",
        to_field_name="id",
        queryset=Product.objects.all(),
    )

    class Meta:
        model = Order
        fields = ('status', 'order_amount', 'created_at', 'updated_at', 'positions',)
