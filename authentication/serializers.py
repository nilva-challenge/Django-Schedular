from django.contrib.auth import get_user_model

from rest_framework import serializers

Member = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        member = Member.objects.create_user(username=validated_data['username'],
                                            password=validated_data['password'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'],
                                            email=validated_data['email'],
                                            is_staff=validated_data['is_staff'])
        member.set_permissions()
        return member
