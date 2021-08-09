from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('<str:username>/validate_tasks/', validate_set_of_tasks , name='valid'),
]