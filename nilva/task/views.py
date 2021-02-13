
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task

# Create your views here.

class AllTaskApiView(APIView):
    def get(self,request,format=None):
        try:
            user=request.user
            print(user.first_name)
            if user.is_superuser==True:
                return Response({'data':Task.objects.all()},status=status.HTTP_200_OK)
            else:
                return Response({'data':Task.objects.all().filter(owner_id=user.id)},status=status.HTTP_200_OK)
        except:
            return Response("internal server error")
            
