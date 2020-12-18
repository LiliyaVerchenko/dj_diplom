from rest_framework import serializers
from collection.models import Collection, ProductInCollection
from product.models import Product


class ProductInCollectionSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов в коллекции."""

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product.id"
    )
    name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = ProductInCollection
        fields = ('product_id', 'name')


class CollectionSerializer(serializers.ModelSerializer):
    """Сериализатор коллекции."""

    collections = ProductInCollectionSerializer(many=True, read_only=False)

    class Meta:
        model = Collection
        fields = ('id', 'title', 'text', 'collections', 'created_at', 'updated_at',)

    def create(self, validated_data):
        collections = validated_data.pop("collections")
        collect_new = super().create(validated_data)
        for collect in collections:
            ProductInCollection.objects.create(
                product=collect["product"]["id"],
                collection=collect_new,
            )
        return collect_new

