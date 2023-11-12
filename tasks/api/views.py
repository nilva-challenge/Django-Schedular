from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from tasks.tasks import send_task_email

from .serializers import TaskSerializer


# Task List and Create View
class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_staff:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(owner=request.user)

            # Schedule email if time_to_send is in the future
            if task.time_to_send and task.time_to_send > now():
                send_task_email.apply_async((task.id,), eta=task.time_to_send)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Task Detail, Update, and Delete View
class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, request):
        task = get_object_or_404(Task, pk=pk)
        if request.user.is_staff or task.owner == request.user:
            return task
        else:
            raise PermissionError

    def get(self, request, pk, format=None):
        task = self.get_object(pk, request)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk, request)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            updated_task = serializer.save()

            # Check if time_to_send is updated and in the future
            if 'time_to_send' in serializer.validated_data and updated_task.time_to_send > now():
                send_task_email.apply_async((updated_task.id,), eta=updated_task.time_to_send)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk, request)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
