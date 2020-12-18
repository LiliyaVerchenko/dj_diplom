from django.contrib import admin
from collection.models import Collection, ProductInCollection


class ProductInCollectionInLine(admin.TabularInline):
    model = ProductInCollection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = [ProductInCollectionInLine]