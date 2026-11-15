from django.contrib import admin

from .models import Stage


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'deadline', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'order__design_type')