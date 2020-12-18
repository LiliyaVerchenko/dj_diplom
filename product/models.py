from django.db import models


class Product(models.Model):
    """Товары"""

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(
        max_length=30,
        verbose_name='Наименование'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=10,
        verbose_name='Цена',
        decimal_places=2
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
        return self.name

