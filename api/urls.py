from django.urls import path
from . import views

urlpatterns = [
    path("api/login/", views.loginAPI.as_view(), name="loginAPI"),
    path("api/register/", views.registerAPI.as_view(), name="registerAPI"),
    path("api/task/user/", views.user_task.as_view()),
    path("api/task/all/", views.all_task.as_view()),
]
