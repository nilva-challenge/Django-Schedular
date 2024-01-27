from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer, ChangePasswordSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse


class NormalUserViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    queryset = User.objects.filter(is_superuser=False).all()

    def delete(self, request, *args, **kwargs):
        User.objects.filter(id=self.kwargs['pk']).update(is_deleted=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateListAdminUser(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(is_superuser=True).all()

    def perform_create(self, serializer):
        serializer.validated_data['is_admin_user'] = True
        serializer.save()


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            serialized_user = UserSerializer(user).data

            # Set the access token in the response headers
            response = Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': serialized_user,
            }, status=status.HTTP_200_OK)

            response['Authorization'] = f'Bearer {str(refresh.access_token)}'
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({'detail': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            user = authenticate(username=user.username, password=new_password)
            if user:
                login(request, user)

            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateRetrieveTaskOfOwn(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        request = self.request
        return Task.objects.select_related('owner').filter(owner_id=request.user.id, is_deleted=False).all()

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)


class CreateListTaskForOtherByAdminView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Task.objects.select_related('owner').filter(owner_id=self.kwargs['pk'], is_deleted=False).all()

    def perform_create(self, serializer):
        serializer.save(owner_id=self.kwargs['pk'], is_done=True)


class RetrieveUpdateDestroyTaskForOtherByAdminView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return (
            Task.objects.select_related('owner')
            .filter(id=self.kwargs["pk"], is_deleted=False).all()
        )

    def delete(self, request, *args, **kwargs):
        Task.objects.select_related('owner').filter(id=self.kwargs['pk']).update(is_deleted=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

