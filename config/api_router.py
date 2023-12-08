from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from task.views import TaskValidatorAPIView

urlpatterns = [
    path("validator", TaskValidatorAPIView.as_view(), name="task_validator"),
]

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)

# urlpatterns += router.urls
