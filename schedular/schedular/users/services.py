from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import Http404
from django.db import transaction
from typing import Dict, Union

User = get_user_model()


@transaction.atomic
def register(data: Dict[str, any]) -> User:
    data.pop('confirm_password')
    user = User.objects.create_user(**data, is_staff=True)
    return user


def login_user(request, data: Dict[str, any]) -> Union[Dict[str, str] | Http404]:
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = {'refresh': str(refresh), 'access': str(refresh.access_token)}
        return access_token
    else:
        raise Http404()
