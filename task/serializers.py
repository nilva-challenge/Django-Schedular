from rest_framework import serializers
from .models import Task



class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'owner', 'time_to_send', 'pre_task']