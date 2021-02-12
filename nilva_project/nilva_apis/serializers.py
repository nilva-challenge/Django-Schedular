from rest_framework.serializers import ModelSerializer
from todo_scheduler.models import Todo
from nilva_accounts.models import User


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"