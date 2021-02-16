from django.contrib import admin

from .models import Task


@admin.register(Task)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'time_to_send')
    ordering = ('time_to_send', 'title')
    search_fields = ('title', 'description', 'owner')
    list_filter = ('owner', 'time_to_send')
    list_per_page = 20
