from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'account'

urlpatterns = [
    path('', register , name='register'),
    path('login/', LoginUserView.as_view()
    , name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html") , name='userlogout'),
]