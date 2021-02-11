from django.contrib import admin
from .models import CustomUser, Task
# Register your models here.


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    filter_horizontal = ['groups', 'user_permissions']
    list_display = ('username', 'role',)
    exclude = ('user_permissions',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'timeToSend')

    def get_queryset(self, request):
        print(request)
        qs = super(TaskAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(owner=request.user)
