from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Custom permission to check if the user has 'admin' permission.
    """

    def has_permission(self, request, view):
        """
        Check if the user has 'admin' permission.

        Args:
            request: The request object.
            view: The view object.

        Returns:
            bool: True if the user has 'admin' permission, False otherwise.
        """
        return request.user.permissions == 'admin'
