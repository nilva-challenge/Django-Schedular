from main.views import *
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views
from django.urls import path

urlpatterns = [
    url(r'^users/$', SignUpUser.as_view()),
    url(r'^tasks/$', GetTasks.as_view()),
]
