from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'design_type', 'client', 'designer',
        'price', 'is_urgent', 'deadline',
    )
    list_filter = ('is_urgent', 'design_type')
    search_fields = ('design_type', 'client__name', 'designer__name')