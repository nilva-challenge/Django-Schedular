from djoser.serializers import UserDeleteSerializer as BaseUserDeleteSerializer, UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from core.models import User


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'admin']

    admin = serializers.SerializerMethodField(method_name='is_admin')

    def is_admin(self, user: User):
        return user.is_superuser


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):

        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'admin']

    admin = serializers.SerializerMethodField(method_name='is_admin')

    def is_admin(self, user: User):
        return user.is_superuser



class UserDeleteSerializer(BaseUserDeleteSerializer):

    current_password = None

    class Meta:
        model = User