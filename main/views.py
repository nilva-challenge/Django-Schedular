from django.shortcuts import render
from .models import Task, User
from .forms import TaskCreateForm, UserCreateForm
from .mixins import AccessRequiredMixin, AdminRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView
)
from django.core.mail import send_mail

class TaskListView(ListView):
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user
        keyword = self.request.GET.get('keyword')
        user_tasks = Task.objects.get_user_tasks(user, keyword) 
        send_mail(
            'fuck',
            'is done',
            'lyrdaq777@gmail.com',
            ['eca9cd61b8@firemailbox.club'],
            fail_silently=False,
        )
        return user_tasks


class TaskDetailView(AccessRequiredMixin, DetailView):
    context_object_name = 'task'
    template_name = 'task/task_detail.html'
   
    def get_object(self):
        pk = self.kwargs['pk']
        queryset = Task.objects.get_task_by_id(pk)     
        return queryset
    

class TaskCreateView(CreateView):
    model = Task
    template_name = 'task/task_create.html'
    form_class = TaskCreateForm

    def form_valid(self,form):
        form.validation(self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class TaskUpdateView(AccessRequiredMixin, UpdateView):
    model = Task
    template_name = 'task/task_update.html'
    form_class = TaskCreateForm

    def form_valid(self,form):
        form.validation(self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.init_owner(self.request, self.object)
        return form


class TaskDeleteView(AccessRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/task_delete.html'
    success_url = '/'


class UserListView(AdminRequiredMixin, ListView):
    template_name = 'user/index.html'
    context_object_name = 'users'
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user
        keyword = self.request.GET.get('keyword')
        user_tasks = User.get_all_users(keyword) 
        return user_tasks


class UserDetailView(AdminRequiredMixin, DetailView):
    template_name = 'user/user_detail.html'
   
    def get_object(self):
        pk = self.kwargs['pk']
        queryset = User.get_user_by_id(pk)     
        return queryset


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    template_name = 'user/user_create.html'
    form_class = UserCreateForm


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    template_name = 'user/user_update.html'
    form_class = UserCreateForm


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'user/user_delete.html'
    success_url = '/users'