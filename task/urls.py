from django.urls import path

from task.views import TaskValidatorAPIView

urlpatterns = [
    path("validator", TaskValidatorAPIView.as_view(), name="task_validator"),
]

# if settings.DEBUG:
#     router = DefaultRouter()
# else:
#     router = SimpleRouter()

# router.register("task", MainCatViewSet)

# app_name = "task"
# urlpatterns += router.urls
