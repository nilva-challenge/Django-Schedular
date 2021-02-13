from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from task.models import Task


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )

        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
