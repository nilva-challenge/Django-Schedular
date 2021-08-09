from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', TaskListView.as_view() , name='index'),
    path('task/create/', TaskCreateView.as_view() , name='create'),
    path('task/<int:pk>/', TaskDetailView.as_view() , name='detail'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view() , name='delete'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view() , name='update'),

    path('users/', UserListView.as_view() , name='uindex'),
    path('user/create/', UserCreateView.as_view() , name='ucreate'),
    path('user/<int:pk>/', UserDetailView.as_view() , name='udetail'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view() , name='udelete'),
    path('user/<int:pk>/update/', UserUpdateView.as_view() , name='uupdate'),
]