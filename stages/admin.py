from django.contrib import admin

from .models import Stage


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'deadline', 'status', 'created_at')
    list_display_links = ('id', 'name')
    list_editable = ('status',)
    list_filter = ('status', 'deadline')
    search_fields = ('name', 'order__design_type', 'order__client__name')
    date_hierarchy = 'deadline'
    autocomplete_fields = ('order',)