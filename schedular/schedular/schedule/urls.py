from django.urls import path
from .apis import TaskAPI


urlpatterns = [
    path('task/', TaskAPI.as_view(), name='taask'),
    path('task/<int:id>/', TaskAPI.as_view(), name='taask'),
]
