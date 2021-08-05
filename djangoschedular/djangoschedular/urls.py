from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken import views


urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", views.obtain_auth_token),
    path('',include('djangoapi.urls',namespace='api')),
    path('', include('pages.urls')),
]
