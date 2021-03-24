from django.http import JsonResponse
from rest_framework import status
from .serializer import RegistrationSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse(UserSerializer(user).data, safe=False, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors)
