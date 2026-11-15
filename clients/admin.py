from django.contrib import admin

from .models import Client
from orders.models import Order


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ('design_type', 'price', 'is_urgent', 'deadline', 'status')
    readonly_fields = ('design_type',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'slug', 'orders_count', 'created_at')
    list_display_links = ('id', 'name')
    list_editable = ('phone',)
    search_fields = ('name', 'phone', 'slug')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('name',)}
    inlines = [OrderInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_orders_count=__import__('django').db.models.Count('orders'))

    @admin.display(description='Заказов', ordering='_orders_count')
    def orders_count(self, obj):
        return obj._orders_count