from django.http import Http404
from .models import Task

class AccessRequiredMixin:
    
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user_id = request.user.id
        if request.user.permission == 'A':
            return super().dispatch(request, *args, **kwargs)

        is_access = Task.objects.query_exists(pk, user_id)
        if is_access:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('you dont have access to see this page')


class AdminRequiredMixin:
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.permission == 'A':
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('you dont have access to see this page')