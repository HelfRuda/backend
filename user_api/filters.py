from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    price = filters.NumberFilter(field_name="price", lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['name', 'description', 'composition', 'discount', 'quantity', 'weight', 'price', 'manufacture_date', 'expiry_date', 'seller', 'category']
