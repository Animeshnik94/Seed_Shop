from django.db import models
from django.conf import settings
from goods.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг', choices=[(i, i) for i in range(1, 6)])  # Рейтинг от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']  # Сортировка по дате создания (новые сверху)

    def __str__(self):
        return f'Отзыв от {self.user.username} на {self.product.name}'