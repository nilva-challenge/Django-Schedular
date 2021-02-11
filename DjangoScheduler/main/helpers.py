from rest_framework_simplejwt.tokens import RefreshToken

GROUP_ROLES = {'A': 'admin', 'N': 'normal'}
GROUP_ROLES_REVERSED = {'admin': 'A', 'normal': 'N'}


def get_token(CustomUser):
    refresh = RefreshToken.for_user(CustomUser)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
