from django.contrib import admin
from order.models import Order, ProductOrderPosition


class ProductOrderPositionInLine(admin.TabularInline):
    model = ProductOrderPosition


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'order_amount', 'status', 'created_at', 'updated_at']
    list_filter = ['client', 'created_at', 'updated_at']
    inlines = [ProductOrderPositionInLine]
