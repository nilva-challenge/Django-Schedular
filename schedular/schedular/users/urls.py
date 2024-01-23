from django.urls import path
from .apis import RegisterApi, LoginAPI


urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('login/', LoginAPI.as_view(), name="login"),
]
