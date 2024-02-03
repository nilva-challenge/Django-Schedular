from rest_framework import serializers
from .models import Task, TaskValidator

class TaskSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'owner', 'time_to_send', 'precondition_tasks', 'is_valid']

    def get_is_valid(self, obj):
        task = TaskValidator(obj)
        is_valid = task.is_valid()
        return 'yes' if is_valid else 'no'