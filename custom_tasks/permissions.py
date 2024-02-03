from rest_framework import permissions
from .models import Task

class TaskPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Allow admin users to perform any action
        if user.permissions == 'admin':
            return True
        # Allow normal users to view their own tasks
        elif user.permissions == 'normal':
            return obj.owner == user

        # Deny permission for any other cases
        return False