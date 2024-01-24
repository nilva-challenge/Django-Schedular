from django.urls import path
from .apis import TaskAPI, ValidateTaskAPI


urlpatterns = [
    path('task/', TaskAPI.as_view(), name='task'),
    path('task/<int:id>/', TaskAPI.as_view(), name='task-detail'),
    path('validator/', ValidateTaskAPI.as_view(), name='task-validator'),
]
