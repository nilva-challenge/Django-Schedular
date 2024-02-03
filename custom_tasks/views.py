from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .permissions import TaskPermission


class TaskList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermission]

    def get_queryset(self):
        user = self.request.user

        # Check if the user is an admin
        if user.permissions == 'admin':
            return Task.objects.all()
        # If the user is a normal user, only show their tasks
        elif user.permissions == 'normal':
            return Task.objects.filter(owner=user)

        # Return an empty queryset if the user has no valid role
        return Task.objects.none()