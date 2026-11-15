from django.contrib import admin

from .models import Designer


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization')
    search_fields = ('name', 'specialization')