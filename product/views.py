from django.shortcuts import render
from product.models import Product
from rest_framework.viewsets import ModelViewSet
from product.serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser
from product.filters import ProductFilter


class ProductViewSet(ModelViewSet):
    """ViewSet для товаров."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return []

