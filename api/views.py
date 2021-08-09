from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import Task


@api_view(['POST'])
def validate_set_of_tasks(request, username):
    
    tasks = Task.objects.filter(owner__username=username)
    for task in tasks:
        for pre_task in task.precondition_tasks.all():
            if pre_task.time_to_send >= task.time_to_send:
                return Response({'validate result':'No'})

    return Response({'validate result':'Yes'})
