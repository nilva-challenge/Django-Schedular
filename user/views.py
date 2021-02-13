from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.
def mylogin(request):
    print(request.user)
    if request.method == "POST":

        utxt = request.POST.get("username")
        ptxt = request.POST.get("password")

        if utxt != "" and ptxt != "":

            user = authenticate(username=utxt, password=ptxt)
            if user != None:
                login(request, user)
                return redirect("panel")

    return render(request, "mylogin.html")


@login_required(login_url="/login/")
def panel(request):

    return render(request, "panel/home.html")


def mylogout(request):
    logout(request)
    return redirect("mylogin")


@login_required(login_url="/login/")
def manager_list(request):

    if request.user.is_superuser == True:
        pass
    if request.user.is_superuser == False:

        error = "Access Diend"
        return render(request, "panel/error.html", {"error": error})

    manager = Profile.objects.all().exclude(user=request.user)
    return render(request, "panel/manager_list.html", {"manager": manager})


@login_required(login_url="/login/")
def user_add(request):

    if request.user.is_superuser == True:
        pass
    if request.user.is_superuser == False:

        error = "Access Diend"
        return render(request, "panel/error.html", {"error": error})

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        utext = request.POST.get("utext")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        permissions = request.POST.get("permissions")
        if pass1 != pass2:
            error = "Your Passr Didn't Match"
            return render(request, "panel/error.html", {"error": error})

        if (
            len(User.objects.filter(username=utext)) == 0
            and len(User.objects.filter(email=email)) == 0
        ):
            if permissions == "Normal":
                user = User.objects.create_user(
                    username=utext, password=pass1, email=email
                )
                b = Profile.objects.get(user=user)
                b.first_name = first_name
                b.last_name = last_name
                b.permissions = permissions
                b.save()
            if permissions == "Admin":
                user = User.objects.create_superuser(
                    username=utext, password=pass1, email=email
                )
                b = Profile.objects.get(user=user)
                b.first_name = first_name
                b.last_name = last_name
                b.permissions = permissions
                b.save()
            return redirect("manager_list")

        else:
            error = "this username or email is already exist"
            return render(request, "panel/error.html", {"error": error})

    return render(request, "panel/user_add.html")


@login_required(login_url="/login/")
def user_del(request, pk):
    if request.user.is_superuser == True:
        pass
    if request.user.is_superuser == False:
        error = "Access Diend"
        return render(request, "panel/error.html", {"error": error})
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return redirect("manager_list")
    except:
        error = "User Not Found"
        return render(request, "panel/error.html", {"error": error})


def myregister(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        utext = request.POST.get("uname")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        if pass1 != pass2:
            error = "Your Pass Didn't Match"
            return render(request, "panel/error.html", {"error": error})

        if (
            len(User.objects.filter(username=utext)) == 0
            and len(User.objects.filter(email=email)) == 0
        ):
            user = User.objects.create_user(username=utext, password=pass1, email=email)
            b = Profile.objects.get(user=user)
            b.first_name = first_name
            b.last_name = last_name
            b.save()

            user1 = authenticate(username=utext, password=pass1)
            if user1 != None:
                login(request, user1)
                return redirect("panel")

        else:
            error = "this username or email is already exist"
            return render(request, "panel/error.html", {"error": error})
    return render(request, "mylogin.html")
