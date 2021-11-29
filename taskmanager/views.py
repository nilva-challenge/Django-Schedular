from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from .models import User, Task
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class SignUp(APIView):
    def post(self, request):
        data = request.data
        serializer = SignUpUserSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.create_user(
                password=data['password'], email=data['email'],
                username=data['username'], first_name=data['first_name'], last_name=data['last_name'],
                permissions=data['permissions'], is_staff=True, is_superuser=True)
            token, create = Token.objects.get_or_create(user=user)
            return Response({token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    def post(self, request):
        try:
            data = request.data
            password = data['password']
            username = data['username']
            user = User.objects.filter(username=username).first()
            if user is None:
                return Response("username is wrong ", status=status.HTTP_400_BAD_REQUEST)
            if user.check_password(raw_password=password):
                token = Token.objects.filter(user=user).first()
                data = {}
                data['token'] = token.key
                data['username'] = user.username
                data['id'] = user.id
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("password is wrong", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response("invalid data")
        
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_task(request):
    data = request.data
    user = request.user
    data['owner_id'] = user.id
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        task = serializer.create(serializer.validated_data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"status": 3000}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def delete_task(request, task_id):
    user = request.user
    try:
        task = Task.objects.filter(pk=task_id, owner_id=user.id).first()
        if task is None:
            return Response({"status": 3003}, status=status.HTTP_400_BAD_REQUEST)
        task.delete()
        return Response({"status": 3000}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"status": 3004}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_task(request, task_id):
    try:
        task = Task.objects.filter(pk=task_id).first()
        if task is None:
            return Response({"status": 3003}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskSerializer_out(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({"status": 3001}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_task(request, task_id):
    user = request.user
    try:
        task = Task.objects.filter(pk=task_id, owner_id=user.id).first()
        if task is None:
            return Response({"status": 2001}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.update(task, serializer.validated_data)
        return Response({"status": 2000}, status=status.HTTP_200_OK)
    except:
        print("esit task error: ", serializer.errors)
        return Response({"status": 2002}, status=status.HTTP_400_BAD_REQUEST)

