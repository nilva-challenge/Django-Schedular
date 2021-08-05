from django.urls import path
from . import views


urlpatterns = [
    
    path('all', views.AllTaskApiView().as_view(),name='all_tasks'),
  
]
