from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    is_staff = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 're_password', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        is_staff = False
        if 'is_staff' in self.validated_data:
            is_staff = self.validated_data['is_staff']
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            is_staff=is_staff
        )
        pas1 = self.validated_data['password']
        pas2 = self.validated_data['re_password']

        """ confirm password """
        if pas1 != pas2:
            raise serializers.ValidationError({'password': 'password are not match'})

        user.set_password(pas1)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']
