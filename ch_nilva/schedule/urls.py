from django.urls import path
from .views import TaskList, index

urlpatterns = [
    path('', TaskList.as_view(), name='all tasks'),
    path('index/', index, name='index')
]
