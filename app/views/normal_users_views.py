from rest_framework import generics
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from ..serializers import *
from ..models import Task
from ..tasks import send_email

User = get_user_model()


class TaskListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating tasks owned by the authenticated user.

    Inherits:
        generics.ListCreateAPIView

    Attributes:
        serializer_class (TaskSerializer): The serializer class for Task model.
        permission_classes (list): The list of permission classes, allowing only authenticated users.

    Methods:
        get_queryset(): Returns the queryset of tasks owned by the authenticated user.
        perform_create(serializer): Performs the creation of a new task and schedules an email notification.

    Note:
        This view requires authentication for listing and creating tasks.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset of tasks owned by the authenticated user.

        Returns:
            QuerySet: The queryset of Task objects.
        """
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Perform the creation of a new task and schedule an email notification.

        Args:
            serializer (TaskSerializer): The serializer instance for the new task.

        Returns:
            None
        """
        task = serializer.save(owner=self.request.user)

        now = timezone.now()
        duration = task.time_to_send - now

        send_email.apply_async(
            args=[task.title, task.description, task.owner.email, task.id],
            countdown=int(duration.total_seconds())
        )


class TaskRetrieveView(generics.RetrieveAPIView):
    """
    API view for retrieving a single task owned by the authenticated user.

    Inherits:
        generics.RetrieveAPIView

    Attributes:
        serializer_class (TaskSerializer): The serializer class for Task model.
        permission_classes (list): The list of permission classes, allowing only authenticated users.

    Methods:
        get_queryset(): Returns the queryset of tasks owned by the authenticated user.

    Note:
        This view requires authentication for retrieving tasks.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset of tasks owned by the authenticated user.

        Returns:
            QuerySet: The queryset of Task objects.
        """
        return Task.objects.filter(owner=self.request.user)
