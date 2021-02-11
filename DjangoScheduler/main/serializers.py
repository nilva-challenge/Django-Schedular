from rest_framework import serializers
from .models import CustomUser, Task
from django.contrib.auth.hashers import make_password


class CreateUser(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password',
                  'email',
                  'role')

    def create(self, validated_data):

        role = None
        
        if 'role' in validated_data:
            role = validated_data['role']
        else:
            role = 'N'

        user = CustomUser.objects.create(first_name=validated_data['first_name'],
                                         last_name=validated_data['last_name'],
                                         username=validated_data['username'],
                                         email=validated_data['email'],
                                         role=role,
                                         is_staff=True,
                                         password=make_password(validated_data['password']))

        user.save()
        return user


class GetTasks(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
