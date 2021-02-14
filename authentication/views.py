from django.shortcuts import render

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        member = serializer.save()
        return Response(member, status=status.HTTP_201_CREATED)
