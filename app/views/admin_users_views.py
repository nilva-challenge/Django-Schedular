from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from ..models import Task
import app.custom_permissions as custom_perms
from ..tasks import send_email
from ..serializers import UserSerializer, TaskAdminSerializer
User = get_user_model()


class UserListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating users. Admins have full control over users.

    Inherits:
        generics.ListCreateAPIView

    Attributes:
        serializer_class (UserSerializer): The serializer class for User model.
        permission_classes (list): The list of permission classes.
            Admins have full control, while others have read-only access.

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          custom_perms.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a user. Admins have full control.

    Inherits:
        generics.RetrieveUpdateDestroyAPIView

    Attributes:
        serializer_class (UserSerializer): The serializer class for User model.
        permission_classes (list): The list of permission classes.
            Admins have full control, while others have read-only access.

    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          custom_perms.IsAdminUser]


class TaskAdminListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating tasks. Admins have full control over tasks.

    Inherits:
        generics.ListCreateAPIView

    Attributes:
        serializer_class (TaskSerializer): The serializer class for Task model.
        permission_classes (list): The list of permission classes.
            Admins have full control, while others have read-only access.

    Methods:
        get_queryset(): Returns the queryset of Task objects.
        perform_create(serializer): Performs the creation of a new task and schedules an email notification.
    """

    serializer_class = TaskAdminSerializer
    permission_classes = [permissions.IsAuthenticated,
                          custom_perms.IsAdminUser]

    def get_queryset(self):
        """
        Get the queryset of Task objects.

        Returns:
            QuerySet: The queryset of Task objects.
        """
        return Task.objects.all()

    def perform_create(self, serializer):
        """
        Perform the creation of a new task and schedule an email notification.

        Args:
            serializer (TaskSerializer): The serializer instance for the new task.

        Returns:
            None
        """
        task = serializer.save()

        now = timezone.now()
        duration = task.time_to_send - now

        send_email.apply_async(
            args=[task.title, task.description, task.owner.email, task.id],
            countdown=int(duration.total_seconds())
        )


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a task. Admins have full control.

    Inherits:
        generics.RetrieveUpdateDestroyAPIView

    Attributes:
        serializer_class (TaskSerializer): The serializer class for Task model.
        permission_classes (list): The list of permission classes.
            Admins have full control, while others have read-only access.

    Methods:
        get_queryset(): Returns the queryset of Task objects.
        perform_update(serializer): Performs the update of a task and reschedules email notification if necessary.
    """

    serializer_class = TaskAdminSerializer
    permission_classes = [permissions.IsAuthenticated,
                          custom_perms.IsAdminUser]

    def get_queryset(self):
        """
        Get the queryset of Task objects.

        Returns:
            QuerySet: The queryset of Task objects.
        """
        return Task.objects.all()

    def perform_update(self, serializer):
        """
        Perform the update of a task and reschedules email notification if necessary.

        Args:
            serializer (TaskSerializer): The serializer instance for the task update.

        Returns:
            None
        """
        task = serializer.save()

        # Reschedule email notification if 'time_to_send' has changed
        if serializer.initial_data.get('time_to_send') != task.time_to_send:
            now = timezone.now()
            duration = task.time_to_send - now

            send_email.apply_async(
                args=[task.title, task.description, task.owner.email, task.id],
                countdown=int(duration.total_seconds())
            )
