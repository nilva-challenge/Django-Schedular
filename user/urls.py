from django.urls import path
from . import views
urlpatterns = [
    path('panel/',views.panel,name='panel'),
    path('login/',views.mylogin,name='mylogin'),
    path('logout',views.mylogout,name='mylogout'),



]