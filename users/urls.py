from django.urls import path
from . import views

urlpatterns = [
    path('normal_user/', views.NormalUserViewSet.as_view(), name='create_list_normal_user'),
    path('normal_user/<uuid:pk>/', views.NormalUserViewSet.as_view(), name='update_retrieve_destroy_normal_user'),
    path('admin_user/', views.CreateListAdminUser.as_view(), name='admin-user'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('tasks/', views.CreateRetrieveTaskOfOwn.as_view(), name='create_list_tasks'),
    path('tasks/user/<uuid:pk>/', views.CreateListTaskForOtherByAdminView.as_view(),
         name='create_list_other_task_by_admin'
         ),
    path('tasks/<uuid:pk>/', views.RetrieveUpdateDestroyTaskForOtherByAdminView.as_view(),
         name='update_retrieve_destroy_task_by_admin'
         )
]
