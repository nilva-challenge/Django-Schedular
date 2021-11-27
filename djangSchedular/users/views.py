from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from .forms import Userform

Profiles = Profile.objects.all()

def profiles (request):
    context = {'profiles':Profiles}
    return render(request,'users/profiles.html',context)


def profile (request,pk):
    profileobj =Profile.objects.get(id=pk)
    return render(request,'users/profile.html',{'profile':profileobj})

def loginPage(request):
   

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            print("username does not exist")
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            print('username or password is incorrect')
    return render(request,'users/login_register.html')





def createUser(request):
    form = UserCreationForm

    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form' : form}
    return render(request,"users/register.html",context) 