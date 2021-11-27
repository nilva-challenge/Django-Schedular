from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    path('tasks/',views.tasks,name = "tasks"),
    path('task/<str:pk>/', views.task, name="task"),
    path('', views.tasks, name="tasks"),
    path('create-task/', views.createTask, name="create-task"),


]

