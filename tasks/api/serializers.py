from rest_framework import serializers
from tasks.models import Task
from django.core.exceptions import ValidationError

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'owner', 'time_to_send', 'pre_tasks']

    def validate(self, data):
        # Validate pre-tasks
        pre_tasks = data.get('pre_tasks', [])

        if self.instance:  # Check if it's an update operation
            if self.instance in pre_tasks:
                raise serializers.ValidationError("A task cannot be a pre-task of itself.")

            # Optional: Check if pre-tasks have a 'time_to_send' before this task
            for pre_task in pre_tasks:
                if pre_task.time_to_send >= data['time_to_send']:
                    raise serializers.ValidationError(f"Pre-task {pre_task.id} must have a 'time_to_send' before this task.")

        return data
