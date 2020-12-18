from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from order.models import Order
from order.serializers import OrderSerializer
from order.filters import OrderFilter
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return []

    def get_queryset(self):
        """Получение списка заказов."""

        if self.request.user.is_superuser:
            return Order.objects.prefetch_related('orders_in').all()
        if self.request.user.is_authenticated:
            return Order.objects.prefetch_related('orders_in').filter(client=self.request.user.id)
        else:
            raise ValidationError("Для работы с заказом необходимо авторизоваться.")





