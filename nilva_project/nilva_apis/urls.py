from django.urls import path
from .views import AllTasksView , UserTasksView , UserRegisterView


app_name = "api"
urlpatterns = [
    path("all_tasks/",AllTasksView.as_view(),name="all_tasks"),
    path("user_tasks/",UserTasksView.as_view(),name="user_tasks"),
    path("register/",UserRegisterView.as_view(),name="user_register"),
]
