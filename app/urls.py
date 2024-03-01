from django.urls import path
from .views import *

urlpatterns = [
    path("task/create/", TaskListCreateView.as_view()),
    path("task/edit/<int:pk>/", TaskRetrieveView.as_view()),

    path("user/admin/list/", UserListCreateView.as_view()),
    path("user/admin/edit/<int:pk>/", UserRetrieveUpdateDestroyView.as_view()),
    path("task/admin/list/", TaskAdminListCreateView.as_view()),
    path("task/admin/edit/<int:pk>/", TaskRetrieveUpdateDestroyView.as_view()),

]
