from main.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^users/$', SignUpUser.as_view()),
]
