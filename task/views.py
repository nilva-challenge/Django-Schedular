from django.shortcuts import render, redirect
from .models import Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission
from datetime import datetime
from django.http import HttpResponse
import csv

# Create your views here.
@login_required(login_url="/login/")
def tasks_list(request):
    if request.user.is_superuser == True:
        tasks = Task.objects.all()

    if request.user.is_superuser == False:
        tasks = Task.objects.filter(owner=request.user)

    """paginator  
    paginator = Paginator(task, 2)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except EmptyPage:
        tasks = paginator.page(paginator.num_page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    """

    return render(request, "panel/tasks_list.html", {"tasks": tasks})


@login_required(login_url="/login/")
def tasks_add(request):

    print(datetime.now().strftime("%H:%M"))
    User = get_user_model()
    user = User.objects.all()
    is_super = request.user.is_superuser
    if is_super == False:
        owner_ins = request.user

    if request.method == "POST":
        title = request.POST.get("title")
        descriptions = request.POST.get("descriptions")
        owner = request.POST.get("owner")
        try:
            owner_ins = User.objects.get(pk=owner)
        except:
            pass
        time_to_send = request.POST.get("time_to_send")

        b = Task(
            title=title,
            descriptions=descriptions,
            time_to_send=time_to_send,
            owner=owner_ins,
        )
        b.save()

        return redirect("tasks_list")

    return render(request, "panel/tasks_add.html", {"user": user})


@login_required(login_url="/login/")
def tasks_del(request, pk):

    if request.user.is_superuser == True:
        pass
    b = Task.objects.get(pk=pk).owner
    if request.user.is_superuser == False:
        if str(request.user) != str(b):
            error = "Access Diend"
            return render(request, "panel/error.html", {"error": error})

    try:

        b = Task.objects.get(pk=pk)
        b.delete()

    except:

        error = "Somthing Wrong"
        return render(request, "panel/error.html", {"error": error})

    return redirect("news_list")


@login_required(login_url="/login/")
def tasks_edit(request, pk):

    print(Task.objects.get(pk=pk).time_to_send)
    if len(Task.objects.filter(pk=pk)) == 0:
        error = "task Not Found"
        return render(request, "panel/error.html", {"error": error})

    if request.user.is_superuser == True:
        pass
    try:
        b = Task.objects.get(pk=pk).owner
    except:
        pass
    if request.user.is_superuser == False:
        owner_ins = request.user
        if str(request.user) != str(b):
            error = "Access Diend"
            return render(request, "panel/error.html", {"error": error})

    User = get_user_model()
    user = User.objects.all()

    try:
        tasks = Task.objects.get(pk=pk)
    except:
        pass

    if request.method == "POST":

        title = request.POST.get("title")
        owner = request.POST.get("owner")
        descriptions = request.POST.get("descriptions")
        time_to_send = request.POST.get("time_to_send")
        try:
            owner_ins = User.objects.get(pk=owner)
        except:
            pass

        if title == "" or descriptions == "" or time_to_send == "":
            error = "All Fields Requirded"
            return render(request, "panel/error.html", {"error": error})

        try:
            b = Task.objects.get(pk=pk)
            b.title = title
            b.descriptions = descriptions
            b.owner = owner_ins
            b.time_to_send = time_to_send

            b.save()

            return redirect("tasks_list")

        except:

            pass

    return render(
        request, "panel/tasks_edit.html", {"pk": pk, "tasks": tasks, "user": user}
    )


@login_required(login_url="/login/")
def export_tasks_csv(request):
    responde = HttpResponse(content_type="text/csv")
    responde["Content_Disposition"] = 'attachment;filename="newslist.csv"'
    writer = csv.writer(responde)
    writer.writerow(["title", "owner", "time to send", "description"])
    if request.user.is_superuser == True:
        tasks = Task.objects.all()
        for i in tasks:
            writer.writerow([i.title, i.owner, i.time_to_send, i.descriptions])
    if request.user.is_superuser == False:
        tasks = Task.objects.filter(owner=request.user)
        for i in tasks:
            writer.writerow([i.title, i.owner, i.time_to_send, i.descriptions])
    return responde
