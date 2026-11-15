from datetime import date

from django.db import models

from orders.models import Order


class Stage(models.Model):

    STATUS_PLANNED = 'planned'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'

    STATUSES = [
        (STATUS_PLANNED, 'Запланирован'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_DONE, 'Выполнен'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='stages',
        verbose_name='Заказ',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название этапа',
    )
    deadline = models.DateField(
        verbose_name='Дедлайн',
    )
    status = models.CharField(
        max_length=16,
        choices=STATUSES,
        default=STATUS_PLANNED,
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    class Meta:
        verbose_name = 'Этап'
        verbose_name_plural = 'Этапы'
        ordering = ['deadline']

    def __str__(self) -> str:
        return f'Этап #{self.pk} — {self.name}'

    def deadline_status(self, today: date | None = None) -> str:
        if today is None:
            today = date.today()
        diff = (self.deadline - today).days
        if diff < 0:
            return 'Дедлайн просрочен :('
        if diff <= 7:
            return 'Дедлайн скоро!'
        return 'Дедлайн нескоро :)'