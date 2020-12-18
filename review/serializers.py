from rest_framework import serializers
from review.models import Review
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username',)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзывов."""

    author_id = UserSerializer(
        read_only=True, )

    class Meta:
        model = Review
        fields = ('id', 'author_id', 'product_id', 'rating',
                  'text', 'created_at', 'updated_at')

    def get_items(self, obj):
        return obj.product_id.id


    def create(self, validated_data):
        """Метод для создания"""

        validated_data["author_id"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        current_user = self.context["request"].user
        product = self.context["request"].data["product_id"]
        method = self.context["request"].stream.method

        reviews = Review.objects.filter(product_id=product).filter(
            author_id=current_user).count()
        if reviews and method == 'POST':
            raise ValidationError({"Error": "Вы можете оставить только 1 отзыв на данный товар!"})
        return data