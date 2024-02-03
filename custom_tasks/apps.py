from django.apps import AppConfig


class CustomTasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_tasks'

    def ready(self):
        from . import signals