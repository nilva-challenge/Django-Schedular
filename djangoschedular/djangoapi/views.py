
from accounts.models import Tasks
from accounts.models import User
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, UserSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAdmin



class loginAPI(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            print(authenticate(user))
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class registerAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": UserSerializer(user, context=RegisterSerializer.context).data,
                "token": Token.objects.create(user=user).key,
            },
            status=status.HTTP_201_CREATED,
        )


class user_task(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        task = Tasks.objects.filter(owner=user)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class all_task(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


    def get(self, request):

        task = Tasks.objects.all()

        serializer = TaskSerializer(task, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
