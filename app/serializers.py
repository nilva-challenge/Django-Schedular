from rest_framework import serializers
from .models import User, Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Attributes:
        Meta:
            model (User): The User model.
            fields (list): The list of fields to include in the serialized representation.

    Note:
        This serializer is used for User model objects in the context of Django REST Framework.
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'permissions']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Attributes:
        Meta:
            model (Task): The Task model.
            fields (list): The list of fields to include in the serialized representation.
            read_only_fields (list): The list of read-only fields.

    Methods:
        validate(data): Validates the serialized data, checking if the 'time_to_send' is before its precondition tasks.

    Note:
        This serializer is used for Task model objects in the context of Django REST Framework.
    """

    class Meta:
        model = Task
        fields = ['title', 'description',
                  'time_to_send', 'pre_tasks', 'owner', 'sent_at']
        read_only_fields = ['owner', 'sent_at']

    def validate(self, data):
        """
        Validate the serialized data, checking if the 'time_to_send' is before its precondition tasks.

        Args:
            data (dict): The serialized data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the 'time_to_send' is before the precondition tasks.
        """
        pre_tasks = data.get("pre_tasks")
        if pre_tasks:
            for pre_task in pre_tasks:
                if data.get("time_to_send") < pre_task.time_to_send:
                    raise serializers.ValidationError(
                        {'result': 'No', 'detail': 'Time of the validating task is before its precondition tasks.'}
                    )
        return data
