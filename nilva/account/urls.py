from django.urls import path
from account.views import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterApi


urlpatterns = [
    path('api/register', RegisterApi.as_view()),
    path('api/login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
]