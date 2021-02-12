from .interfaces import TodoInterface
from .models import Todo


class TodoService(TodoInterface):
    
    def get_all_todos(self):
        return Todo.objects.all()

    def get_user_todos(self,user):
        return Todo.objects.filter(owner=user)