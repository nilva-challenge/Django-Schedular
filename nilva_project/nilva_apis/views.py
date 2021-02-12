from django.shortcuts import render
from rest_framework.views import APIView
from todo_scheduler.models import Todo
from rest_framework.response import Response
from rest_framework import status
from todo_scheduler.services import TodoService
from .serializers import TodoSerializer , RegisterUserSerializer
from .permissions import IsSuperUser
from rest_framework import permissions
from nilva_accounts.services import UserService

todo_service = TodoService()
user_service = UserService()


class AllTasksView(APIView):
    permission_classes = [IsSuperUser]

    def get(self,request):
        tasks = todo_service.get_all_todos()
        serializer = TodoSerializer(tasks,many=True)
        print(request.user.is_superuser)
        return Response(serializer.data,status.HTTP_200_OK)

class UserTasksView(APIView):

    def get(self,request):
        tasks = todo_service.get_user_todos(request.user)
        serializer = TodoSerializer(tasks,many=True)
        return Response(serializer.data,status.HTTP_200_OK)

class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        try:
            serializer = RegisterUserSerializer(data=request.data)
            if serializer.is_valid():
                password = serializer.validated_data["password"]
                user = serializer.save()
                user_service.hash_password(user,password)
                return Response({"data" : "user successfully created"} , status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"data" : "somethings wrong"},status.HTTP_500_INTERNAL_SERVER_ERROR)