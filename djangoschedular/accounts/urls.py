from django.urls import path
from django.contrib import admin
from .import views
from .views import UseraddTask

urlpatterns=[
     path('register/',views.register, name='register'),
     path('user_register/',views.user_register.as_view(), name='user_register'),
     path('admin_register/',views.admin_register.as_view(), name='admin_register'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('admin/', admin.site.urls),
     path('admin/accounts/user/',views.addordelete,name='addordelete'),
     path('showTasks',views.showTasks,name='showTasks'),
     path('UseraddTask/',views.UseraddTask,name='UseraddTask'),
     path('admin/accounts/tasks/',views.adminaddTask,name='adminaddTask')


]