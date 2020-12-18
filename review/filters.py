from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from review.models import Review
from product.models import Product



class ReviewFilter(filters.FilterSet):
    author_id = filters.ModelChoiceFilter(
        field_name='author_id',
        to_field_name='id',
        queryset=User.objects.all(),
    )
    product_id = filters.ModelChoiceFilter(
        field_name='product_id',
        to_field_name='id',
        queryset=Product.objects.all(),
    )
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Review
        fields = ('author_id', 'product_id', 'created_at',)