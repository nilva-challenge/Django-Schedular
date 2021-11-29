from django.urls import path
from .views import *

app_name = 'taskmanager'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('addtask/', add_task, name='addtask'),
    path('deletetask/<int:task_id>/', delete_task, name='deletetask'),
    path('viewtask/<int:task_id>/', view_task, name='viewtask'),
    path('edittask/<int:task_id>/', edit_task, name='edittask'),
]
