from .models import User
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from drf_spectacular.utils import extend_schema

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class RegisterView(APIView):

    @classmethod
    @extend_schema(responses=UserSerializer)
    def register(cls, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @extend_schema(responses=UserSerializer)
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return self.register(request)
        
        try:
            payload = jwt.decode(token, 'kaboom', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return self.register(request)
        
        raise AuthenticationFailed('Already authenticated, logout!')
    
class LoginView(APIView):

    @extend_schema(responses=UserSerializer)
    def post(self, request):
        try:
            username = request.data['username']
        except KeyError:
            username = None

        try:
            email = request.data['email']
        except KeyError:
            email = None

        password = request.data['password']

        if username is not None:
            user = User.objects.filter(username=username).first()
        elif email is not None:
            user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'kaboom', algorithm='HS256')

        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response
    
class UserView(APIView):

    @extend_schema(responses=UserSerializer)
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'kaboom', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
class LogoutView(APIView):
    
    @extend_schema(responses=UserSerializer)
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Success'
        }
        return response