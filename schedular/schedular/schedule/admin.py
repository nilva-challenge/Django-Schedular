from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'time_to_send', 'sent')

    def get_queryset(self, request):
        # Check if the user is an admin
        if request.user.is_superuser:
            return Task.objects.all()

        # Regular user can only see and edit their own tasks
        return Task.objects.filter(owner=request.user)
