from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название клиента')
    phone = models.CharField(
        max_length=32, blank=True, default='', verbose_name='Телефон',
    )
    slug = models.SlugField(
        max_length=255, unique=True, null=True, blank=True, verbose_name='Slug'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name} ({self.phone})' if self.phone else self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'client'
            slug = base
            n = 1
            while Client.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f'{base}-{n}'
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('clients:detail', kwargs={'slug': self.slug})