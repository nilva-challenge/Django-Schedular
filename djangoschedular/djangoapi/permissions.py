from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view=None):
        if request.user.is_superuser == True:
            return True
        else:
            return False
