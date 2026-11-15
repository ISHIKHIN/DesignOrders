from django.contrib import admin

from .models import Designer
from orders.models import Order


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ('design_type', 'price', 'is_urgent', 'deadline', 'status')
    readonly_fields = ('design_type',)


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization', 'orders_count')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'specialization')
    list_filter = ('specialization',)
    inlines = [OrderInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_orders_count=__import__('django').db.models.Count('orders'))

    @admin.display(description='Заказов', ordering='_orders_count')
    def orders_count(self, obj):
        return obj._orders_count