from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import *
from .models import *
from .helpers import GROUP_ROLES, GROUP_ROLES_REVERSED
from rest_framework.permissions import IsAuthenticated


class GetTasks(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetTasks

    def get_queryset(self):
        print(self.request.user.role)
        user = self.request.user
        if user.role == GROUP_ROLES_REVERSED['admin']:
            return Task.objects.all()
        else:
            return Task.objects.filter(owner=user)


class SignUpUser(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUser
