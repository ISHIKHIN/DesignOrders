from datetime import date

from django.db import models

from orders.models import Order


class StageQuerySet(models.QuerySet):
    def planned(self):
        return self.filter(status=Stage.Status.PLANNED)

    def in_progress(self):
        return self.filter(status=Stage.Status.IN_PROGRESS)

    def done(self):
        return self.filter(status=Stage.Status.DONE)

    def active(self):
        return self.exclude(status=Stage.Status.DONE)

    def for_date(self, target_date):
        return self.filter(deadline=target_date)


class StageManager(models.Manager.from_queryset(StageQuerySet)):
    pass


class Stage(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Запланирован'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE = 'done', 'Выполнен'

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='stages',
        verbose_name='Заказ',
    )
    name = models.CharField(max_length=255, verbose_name='Название этапа')
    deadline = models.DateField(verbose_name='Дедлайн')
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    objects = StageManager()

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
            return 'Дедлайн просрочен'
        if diff <= 7:
            return 'Дедлайн скоро'
        return 'Дедлайн нескоро'