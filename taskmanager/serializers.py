from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, Task
    
   
class SignUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username',
                  'first_name', 'last_name', 'permissions')
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        try:
            instance.first_name = validated_data.get(
                'first_name', instance.first_name)
            instance.last_name = validated_data.get(
                'last_name', instance.last_name)
            instance.email = validated_data.get('email', instance.email)
            instance.username = validated_data.get(
                'username', instance.username)
        except Exception as e:
            raise ValueError(e)
            return False
        instance.save()
        return instance



class TaskSerializer(serializers.ModelSerializer):
    owner_id = serializers.CharField()

    class Meta:
        model = Task
        fields = ('owner_id', 'title', 'description', 'time_to_send')

    def create(self, validated_data):
        owner_id = validated_data.pop('owner_id')
        user = User.objects.filter(id=owner_id).first()
        task = Task(owner=user, **validated_data)
        if task is None:
            raise ValueError('task can not create')
        task.save()
        return task

    def update(self, instance, validated_data):
        try:
            instance.title = validated_data.get(
                'title', instance.title)
            instance.description = validated_data.get(
                'description', instance.description)
            instance.owner_id = validated_data.get('owner_id', instance.owner_id)
            instance.time_to_send = validated_data.get(
                'time_to_send', instance.time_to_send)
        except Exception as e:
            raise ValueError(e)
            return False
        instance.save()
        return instance

class TaskSerializer_out(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username')

    class Meta:
        model = Task
        fields = ['title', 'description', 'time_to_send',
                  'owner_name', 'precondition_tasks']

    
    
