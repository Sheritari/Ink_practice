from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import User

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'kaboom', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        if user.is_authenticated:
            if request.method in permissions.SAFE_METHODS or user.is_staff:
                return True
        return False