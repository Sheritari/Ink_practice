from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Пользователь"""

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    name = models.CharField(max_length=255, verbose_name='Имя пользователя')
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, verbose_name='Пароль')
    username = models.CharField(max_length=255, verbose_name='Логин', unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']