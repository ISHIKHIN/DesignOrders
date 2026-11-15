from django.db import models


class Designer(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name='Имя дизайнера',
    )
    specialization = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name='Специализация',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    class Meta:
        verbose_name = 'Дизайнер'
        verbose_name_plural = 'Дизайнеры'
        ordering = ['name']

    def __str__(self) -> str:
        if self.specialization:
            return f'{self.name} ({self.specialization})'
        return self.name