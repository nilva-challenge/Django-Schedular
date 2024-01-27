from django.shortcuts import get_object_or_404
from .models import Task
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TaskSerializer
from rest_framework import status
from core.models import User
from django.http import HttpRequest
from .tasks import send_status_of_task_email_task
from datetime import datetime
from django.db.models import Q


@api_view()
def check_task_status(request):
    
    user = request.user.id
    user_email = request.user.email
    user_tasks = Task.objects.filter(owner=user)
    today_dateime = datetime.now().strftime("20%y-%m-%d")
    ready_to_send_task = user_tasks.filter(Q(time_to_send__date=today_dateime) & Q(pre_task=None))

    if not ready_to_send_task:
        ready_to_send_task = user_tasks.filter(Q(time_to_send__date=today_dateime) & Q(pre_task__time_to_send__lt=today_dateime))
        print(ready_to_send_task)

    serializer = TaskSerializer(ready_to_send_task, many=True)
    if ready_to_send_task and user_email:
        send_status_of_task_email_task.delay(user_email, f'Done Tasks:\n{serializer.data}')
        return Response(serializer.data)
    else:
        return Response('No Task Done Yet!')


@api_view(['GET', 'POST'])
def task_list(request: HttpRequest):
    filter_by_title = request.query_params.get('title')
    filter_by_id = request.query_params.get('id')

    user: User = request.user
    is_admin: bool = user.is_superuser
    
    if request.method == 'GET':
        if is_admin:
            tasks = Task.objects.all()
            if filter_by_title:
                tasks = tasks.filter(title__icontains=filter_by_title)
            elif filter_by_id:
                tasks = tasks.filter(id=filter_by_id)

        else:
            tasks = Task.objects.filter(owner=request.user.id)
            if filter_by_title:
                tasks = tasks.filter(title__icontains=filter_by_title)
            elif filter_by_id:
                tasks = tasks.filter(id=filter_by_title)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        owner = request.user
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['owner'] = owner
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request: HttpRequest, id):
    user: User = request.user
    task = get_object_or_404(Task, pk=id)
    is_admin: bool = user.is_superuser
    is_owner: bool =  user.id == task.owner.id

    if request.method == 'GET':

        if is_admin or is_owner:
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        else:
            return Response({'error':'You can not see this Task.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    
    elif request.method == 'PUT':
            if is_admin or is_owner:
                serializer = TaskSerializer(instance=task, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'Error':'You Do not have Permission to Update this Task.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    elif request.method == 'DELETE':
        if is_admin or is_owner:
            try:
                task.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            except Exception as e:
                return Response({'error':'Task can not be deleted, because it is associated with another task.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
        else:
            return Response({'Error':'You dont have permissions to delete this task.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)