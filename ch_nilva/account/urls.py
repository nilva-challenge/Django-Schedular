from django.urls import path
from .views import UserRegisterApi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register', UserRegisterApi.as_view(), name='register'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/token', TokenRefreshView.as_view(), name='token_obtain_pair'),
]
