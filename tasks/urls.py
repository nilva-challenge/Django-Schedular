from django.urls import path
from .views import TaskListView


urlpatterns = [
    path('register/', TaskListView.as_view()),
]
