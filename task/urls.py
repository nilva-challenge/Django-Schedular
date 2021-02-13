from django.urls import path
from . import views

urlpatterns = [
    path("panel/tasks/list/", views.tasks_list, name="tasks_list"),
    path("panel/tasks/add/", views.tasks_add, name="tasks_add"),
    path("panel/tasks/del/<int:pk>/", views.tasks_del, name="tasks_del"),
    path("panel/tasks/edit/<int:pk>/", views.tasks_edit, name="tasks_edit"),
    path("panel/tasks/export/", views.export_tasks_csv, name="export_tasks_csv"),
]
