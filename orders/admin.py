from django.contrib import admin

from .models import Order
from stages.models import Stage


class StageInline(admin.TabularInline):
    model = Stage
    extra = 0
    fields = ('name', 'deadline', 'status')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'design_type', 'client', 'designer',
        'price', 'is_urgent', 'status', 'is_expensive', 'deadline',
    )
    list_display_links = ('id', 'design_type')
    list_editable = ('status', 'is_urgent')
    list_filter = ('status', 'is_urgent', 'is_expensive', 'design_type')
    search_fields = ('design_type', 'client__name', 'designer__name')
    date_hierarchy = 'deadline'
    autocomplete_fields = ('client', 'designer')
    inlines = [StageInline]
    fieldsets = (
        ('Основное', {
            'fields': ('client', 'designer', 'design_type', 'price'),
        }),
        ('Сроки и статус', {
            'fields': ('is_urgent', 'deadline', 'status'),
        }),
        ('Служебное', {
            'fields': ('is_expensive', 'created_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('is_expensive', 'created_at')