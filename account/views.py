from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.permission = "N"
            obj.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'create account for {username} successfuly')
            return redirect('main:index')
    else:
        form = UserRegisterForm()
    return render(request, "account/register.html",{"form":form})


class LoginUserView(LoginView):
    template_name = 'account/login.html'

