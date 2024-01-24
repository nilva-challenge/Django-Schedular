from .apis import RegisterApi, LoginAPI
from django.urls import path


urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('login/', LoginAPI.as_view(), name="login"),
]
