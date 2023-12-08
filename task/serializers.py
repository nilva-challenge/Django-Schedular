from rest_framework import serializers


class TaskValidatorSerializer(serializers.Serializer):
    json = serializers.JSONField()
