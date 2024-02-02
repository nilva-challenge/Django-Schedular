
from django.urls import path
from .views import  TaskList

urlpatterns = [
    path('validate/', TaskList.as_view(), name='task-validation'),
]
