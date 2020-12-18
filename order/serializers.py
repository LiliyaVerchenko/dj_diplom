from rest_framework import serializers
from order.models import Order, ProductOrderPosition
from django.contrib.auth.models import User
from product.models import Product


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для пользователя."""

    class Meta:
        model = User
        fields = ('id', )


class ProductOrderPositionSerializer(serializers.Serializer):
    """Сериализатор для позиций в заказе."""

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product.id"
    )
    name = serializers.CharField(
        source="product.name",
        read_only=True
    )
    quantity = serializers.IntegerField(
        min_value=1,
        default=1
    )


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказа."""

    orders_in = ProductOrderPositionSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'client', 'orders_in', 'order_amount', 'status', 'created_at', 'updated_at', )
        read_only_fields = ('client', 'order_amount',)


    def create(self, validated_data, total_price=0):
        """Метод для создания заказа."""

        validated_data["client"] = self.context["request"].user
        products = validated_data.pop("orders_in")
        for product_position in products:
            total_price += product_position["product"]["id"].price * product_position["quantity"]
            validated_data["order_amount"] = total_price
        order = super().create(validated_data)
        for product_position in products:
            ProductOrderPosition.objects.create(
                product=product_position["product"]["id"],
                quantity=product_position["quantity"],
                order=order,
            )
        return order
