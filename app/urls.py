from django.urls import path
from .views import *

urlpatterns = [
    path("task_create/", TaskListCreateView.as_view()),
    path("task_retrieve/<int:pk>/", TaskRetrieveView.as_view())
]
