from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework import serializers

from core.celery import celery_app
from .models import User, Task


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data: dict) -> User:
        is_admin_user = validated_data.pop('is_admin_user', False)
        return (
            User.objects.create_superuser(**validated_data)
            if is_admin_user else
            User.objects.create_user(**validated_data)
        )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_deleted']
        read_only_fields = ['id']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj: Task):
        user = obj.owner
        return UserSerializer(user).data

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'is_done']

    def save(self, **kwargs):
        task: Task = super().save(**kwargs)
        calculate_time_difference = self.calculate_time_difference(time_to_send=task.time_to_send)
        print('alo pepe')
        celery_app.send_task(
            'users.tasks.send_task_email', args=(task.id,), countdown=int(calculate_time_difference.seconds)
        )
        return task

    @staticmethod
    def calculate_time_difference(time_to_send: datetime) -> timedelta:
        return time_to_send - timezone.now()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
