from django.urls import path
from . import views

urlpatterns = [
    path("panel/", views.panel, name="panel"),
    path("", views.mylogin, name="mylogin"),
    path("logout", views.mylogout, name="mylogout"),
    path("panel/manager/list/", views.manager_list, name="manager_list"),
    path("panel/user/add/", views.user_add, name="user_add"),
    path("panel/user/del/<int:pk>/", views.user_del, name="user_del"),
    path("register/", views.myregister, name="myregister"),
]
