from rest_framework import serializers
from account.models import User
from .models import Task


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]


class TaskSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()

    class Meta:
        model = Task
        fields = '__all__'
