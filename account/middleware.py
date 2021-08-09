from django.shortcuts import redirect
from django.urls import reverse

EXCEPTION_PATH = [ 
    '/account/login/',
    '/logout/',
    '/account/'
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if '/api/' in request.path:
            return response 

        if request.path not in EXCEPTION_PATH and not request.user.is_authenticated:
            return redirect(reverse('account:login'))

        return response