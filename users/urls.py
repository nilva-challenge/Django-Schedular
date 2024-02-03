
from django.urls import path
from .views import send_test_email

urlpatterns = [
    path('email/', send_test_email),
]
