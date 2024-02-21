from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import User

def check_jwt(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        payload = jwt.decode(token, 'kaboom', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    user = User.objects.filter(id=payload['id']).first()
    if user.is_authenticated:
        return True, user
    return False, None

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        check = check_jwt(request)
        cheker, user = check[0], check[1]
        if cheker:
            if request.method in permissions.SAFE_METHODS or user.is_staff:
                return True
        return False

class TypeCharacteristicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        check = check_jwt(request)
        cheker, user = check[0], check[1]
        if cheker:
            if user.is_staff or user.groups.all().filter(name='wrk_type_char').exists():
                return True
        return False