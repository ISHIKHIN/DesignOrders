from django.db import models


class Client(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name='Название клиента',
    )
    phone = models.CharField(
        max_length=32,
        blank=True,
        default='',
        verbose_name='Телефон',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name} ({self.phone})' if self.phone else self.name