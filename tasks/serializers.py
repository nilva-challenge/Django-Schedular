from rest_framework import serializers

from .models import Task
from users.serializers import MemberSerializer


class TaskSerializer(serializers.ModelSerializer):
    owner = MemberSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
        }

