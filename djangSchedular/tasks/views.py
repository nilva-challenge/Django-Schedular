from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Task
from .forms import Taskform




Tasks = Task.objects.all()

def tasks (request):
    context = {'tasks':Tasks}
    return render(request,'tasks/tasks.html',context)


def task (request,pk):
    taskobj = Task.objects.get(id=pk)
    return render(request,'tasks/one-task.html',{'task':taskobj})


def createTask(request):
    form = Taskform

    if request.method == 'POST':
        form = Taskform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    context = {'form' : form}
    return render(request,"tasks/task_form.html",context) 