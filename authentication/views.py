from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers as auth_serializers


class RegisterView(generics.CreateAPIView):
    """
        Register a new member with the user data
    """
    permission_classes = (AllowAny,)
    serializer_class = auth_serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_staff = serializer.validated_data['is_staff']
        is_superuser = request.user.is_superuser

        if create_staff and not is_superuser:
            return Response('Only superusers can create new staff members',
                            status=status.HTTP_401_UNAUTHORIZED)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
