from django.db import models
from django.conf import settings
from product.models import Product


class Review(models.Model):
    """Отзывы"""

    CHOICES_RATING = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    author_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    product_id = models.ForeignKey(
        Product, related_name='reviews',
        verbose_name='Товар',
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        choices=CHOICES_RATING,
        verbose_name='Оценка'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
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
        return f"Отзыв от {self.author_id} о {self.product_id}"


