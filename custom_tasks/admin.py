from django.contrib import admin
from .models import Task
from .utils import is_task_owner

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'time_to_send', 'get_pre_tasks_display')

    def get_queryset(self, request):
        # Return all tasks for admin users, no filtering
        if request.user.permissions == 'admin':
            return super().get_queryset(request)
        # Only show tasks belonging to the logged-in user for normal users
        return super().get_queryset(request).filter(owner=request.user)

    def has_view_permission(self, request, obj=None):
        # Check if the user has the required permission to view the task
        return request.user.permissions == 'normal' and (obj is None or is_task_owner(request.user, obj))
    
    def get_pre_tasks_display(self, obj):
        # Custom method to display a string representation of pre_tasks
        return ', '.join([str(task) for task in obj.precondition_tasks.all()])
    
    get_pre_tasks_display.short_description = 'Pre Tasks'
    
    def save_model(self, request, obj, form, change):
        # Set the owner to the logged-in user when creating a new task
        if not change:
            obj.owner = request.user
        obj.save()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Check if the user is an admin
        if not request.user.permissions == 'admin':
            # Exclude the field for non-admin users
            form.base_fields.pop('owner', None)

        return form

admin.site.register(Task, TaskAdmin)