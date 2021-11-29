from django.contrib import admin
from .models import Task, User
from django.contrib import messages


class TaskNormalUser(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return request.user.permissions == 1

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.permissions == 1


class NormalUserAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return request.user.permissions == 1

    def has_view_permission(self, request, obj=None):
        return request.user.permissions == 1

    def has_add_permission(self, request, obj=None):
        return request.user.permissions == 1

    def has_delete_permission(self, request, obj=None):
        return request.user.permissions == 1
    
    


admin.site.register(User, NormalUserAdmin)
admin.site.register(Task, TaskNormalUser)
