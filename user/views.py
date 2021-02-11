from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def mylogin (request):
    if request.method == 'POST' :

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "" :

            user = authenticate(username=utxt, password=ptxt)
            '''
            ip,is_routable=get_client_ip(request)
            responde=DbIpCity.get(ip,api_key='free')
            print(responde)
            '''
            if user !=None:
                login(request,user)
                return redirect('panel')


    return render(request,'mylogin.html')
@login_required(login_url='/login/')
def panel (request):

    return render(request, 'panel/home.html')

def mylogout (request):
    logout(request)
    return redirect('mylogin')
