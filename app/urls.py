from django.urls import path
from .views import *

urlpatterns = [
    path("task/create/", TaskListCreateView.as_view(), name="task_list_create"),
    path("task/edit/<int:pk>/", TaskRetrieveView.as_view(), name="task_edit"),

    path("user/admin/list/", UserListCreateView.as_view(), name="user_list_create"),
    path("user/admin/edit/<int:pk>/",
         UserRetrieveUpdateDestroyView.as_view(), name="user_edit"),
    path("task/admin/list/", TaskAdminListCreateView.as_view(),
         name="admin_task_list_create"),
    path("task/admin/edit/<int:pk>/",
         TaskRetrieveUpdateDestroyView.as_view(), name="admin_task_edit"),
]
