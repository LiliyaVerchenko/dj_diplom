from django.db import models
from django.conf import settings
from product.models import Product


class ProductOrderPosition(models.Model):
    """Товары в заказе"""

    product = models.ForeignKey(
        Product,
        related_name='products_in',
        on_delete=models.CASCADE,
        default=None
    )
    order = models.ForeignKey(
        'Order',
        related_name='orders_in',
        on_delete=models.CASCADE,
        default=None
    )
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    """Работа с заказом"""

    CHOICES_STATUS = (
        ('NEW', 'Новый заказ'),
        ('IN_PROGRESS', 'В обработке'),
        ('DONE', 'Выполнен')
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
    )
    position = models.ManyToManyField(
        Product,
        through=ProductOrderPosition,
        related_name="order"
    )
    status = models.CharField(
        max_length=30,
        verbose_name='Статус заказа',
        choices=CHOICES_STATUS,
        default='NEW'
    )
    order_amount = models.DecimalField(
        max_digits=10,
        verbose_name='Сумма заказа',
        decimal_places=2,
    )
    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True
    )

    def __str__(self):
        return f"Заказ № {self.id} на сумму {self.order_amount}"


