from .models import Task
from .serializer import TaskSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class TaskList(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        query = Task.objects.all()
        if user.is_superuser:
            return query
        elif user.is_admin:
            return query.filter(owner__is_superuser=False)
        else:
            return query.filter(owner=self.request.user)

