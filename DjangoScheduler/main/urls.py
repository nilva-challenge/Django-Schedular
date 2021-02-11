from main.views import *
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views
from django.urls import path

urlpatterns = [
    url(r'^signUp/$', SignUpUser.as_view()),
    url(r'^login/$', jwt_views.TokenObtainPairView.as_view(),
        name='login'),
    url(r'^tasks/$', GetTasks.as_view()),
]
