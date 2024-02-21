from .models import User
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.http import Http404

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
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
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
    def get(self, request, pk=None):
        if pk is not None:
            # Получение информации о конкретном пользователе
            user = User.objects.filter(id=pk).first()
            if not user:
                raise Http404("User does not exist")

            serializer = UserSerializer(user)
        else:
            # Получение списка всех пользователей
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
    
    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Добавление пользователя в группу
        group_name = request.data.get('group')
        if group_name:
            group = Group.objects.filter(name=group_name).first()
            if group:
                group.user_set.add(user)
            else:
                raise ValidationError("Group does not exist")

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def put(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            raise Http404("User does not exist")
        
        # Обновление пользовательских данных
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        
        # Изменение группы пользователя
        group_name = request.data.get('group')
        if group_name:
            group = Group.objects.filter(name=group_name).first()
            if group:
                # Удаляем пользователя из имеющихся групп
                user.groups.clear()
                group.user_set.add(user)
            else:
                raise ValidationError("Group does not exist")
        
        return Response(UserSerializer(updated_user).data)
    
    def delete(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if not user:
            raise Http404("User does not exist")
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class LogoutView(APIView):
    
    @extend_schema(responses=UserSerializer)
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Success'
        }
        return response