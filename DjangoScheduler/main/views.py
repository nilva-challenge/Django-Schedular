from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import * 
from .models import *

class GetTasks(ListAPIView):
    serializer_class = GetTasks

    def get_queryset(self):
        # get token and check if it's admin's or normal user
        pass


class SignUpUser(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUser