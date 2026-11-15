from datetime import date

from django.db import models

from clients.models import Client
from designers.models import Designer


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE = 'done', 'Выполнен'
        CANCELLED = 'cancelled', 'Отменён'

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Клиент',
    )
    designer = models.ForeignKey(
        Designer,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Дизайнер',
    )
    design_type = models.CharField(max_length=64, verbose_name='Тип дизайна')
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Стоимость, руб.',
    )
    is_urgent = models.BooleanField(default=False, verbose_name='Срочный заказ')
    deadline = models.DateField(verbose_name='Дедлайн')
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Статус',
    )
    is_expensive = models.GeneratedField(
        expression=models.Q(price__gte=10000),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name='Дорогой заказ',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['deadline']

    def __str__(self) -> str:
        return f'Заказ #{self.pk} — {self.design_type}'

    def get_status(self) -> str:
        urgency = 'Срочно' if self.is_urgent else 'Не срочно'
        return (
            f'Заказ #{self.pk} {self.design_type} '
            f'({urgency}) на сумму {self.price} руб. '
            f'Срок: {self.deadline:%Y-%m-%d}'
        )

    def deadline_status(self, today: date | None = None) -> str:
        if today is None:
            today = date.today()
        diff = (self.deadline - today).days
        if diff < 0:
            return 'Дедлайн просрочен'
        if diff <= 7:
            return 'Дедлайн скоро'
        return 'Дедлайн нескоро'