from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from schedular.schedule.selectors import get_tasks
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from .services import TaskService
from .models import Task


class TaskAPI(APIView):
    permission_classes = (IsAuthenticated,)

    class InputTaskSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            exclude = ('owner',)

    class OutputTaskSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = '__all__'

    @extend_schema(responses=OutputTaskSerializer)
    def get(self, request):
        query = get_tasks(user=request.user)
        return Response(self.OutputTaskSerializer(query, many=Task).data, status=status.HTTP_200_OK)

    @extend_schema(request=InputTaskSerializer, responses=OutputTaskSerializer)
    def post(self, request):
        data = self.InputTaskSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        task_service = TaskService(user=request.user, data=data.validated_data)
        task = task_service.create_task()
        return Response(self.OutputTaskSerializer(task).data, status=status.HTTP_201_CREATED)

    @extend_schema(request=InputTaskSerializer, responses=OutputTaskSerializer)
    def patch(self, request, id):
        data = self.InputTaskSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        task_service = TaskService(user=request.user, data=data.validated_data, id=id)
        task = task_service.update_task()
        return Response(self.OutputTaskSerializer(task).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        task_service = TaskService(user=request.user, id=id)
        task_service.delete_task()
        return Response(status=status.HTTP_204_NO_CONTENT)
