from .serializer import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .models import User


class UserRegisterApi(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
