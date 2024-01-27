from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('<int:id>/', views.task_detail, name='task-detail'),
    path('task_status/', views.check_task_status, name='task-status'),
]
