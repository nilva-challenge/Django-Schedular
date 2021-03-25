from .models import Task
from .serializer import TaskSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.http.response import HttpResponse


class TaskList(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        query = Task.objects.all()
        if not self.request.is_staff:
            return query.filter(owner=self.request.user)
        return query


from .tasks import sleepy


def index(request):
    sleepy.delay(10)
    return HttpResponse('Nothing')
