from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomerSignUpForm, EmployeeSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User , Tasks
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

def register(request):
    return render(request, '../templates/register.html')

class user_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = '../templates/user_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class admin_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = '../templates/admin_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')


def addordelete(request):
    return render(request,'accounts/admin')

@login_required
def showTasks(request):
    tasks = Tasks.objects.all()
    return render(request,'../templates/showTasks.html',{'tasks':tasks})






list = []



@login_required()
def UseraddTask(request):
    User = get_user_model()
    user = User.objects.all()
    is_super = request.user.is_superuser
    if is_super == False:
        owner_ins = request.user
    if request.method == "POST":
        title = request.POST.get("title")
        descriptions = request.POST.get("descriptions")
        owner = request.POST.get("owner")
        preTask = request.POST.get('preTask')
        list.append(preTask)
        print(list)
        try:
            owner_ins = User.objects.get(pk=owner)
        except:
            pass
        time_to_send = request.POST.get("time_to_send")

        b = Tasks(
            title=title,
            descriptions=descriptions,
            time_to_send=time_to_send,
            owner=owner_ins,
            preTask=preTask,
        )
        b.save()

        return redirect("/")
    return render(request, "../templates/addTask.html", {"user": user})




def adminaddTask(request):
    return render(request, 'accounts/admin')