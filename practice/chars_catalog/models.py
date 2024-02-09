from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import AbstractUser

class CharacteristicType(models.Model):
    """Справочник типов характеристик"""

    class Meta:
        db_table = 'characteristic_types'
        verbose_name = 'Вид характеристики'
        verbose_name_plural = 'Виды характеристик'

    name = models.CharField(max_length=250, unique=True, verbose_name='Название')
    max_value_x = models.PositiveIntegerField(verbose_name='Максимальное значение по оси x')
    max_value_y = models.PositiveIntegerField(verbose_name='Максимальное значение по оси y')
    json_key_name = models.CharField(max_length=250, verbose_name='Ключ в json')
    json_value_name = models.CharField(max_length=250, verbose_name='Значение в json')

    def __str__(self):
        return f"{self.name}"
    
class Characteristic(models.Model):
    """Характеристика"""

    class Meta:
        db_table = 'characteristics'
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    value = JSONField(verbose_name="Значение")
    characteristic_type = models.ForeignKey(CharacteristicType, on_delete=models.CASCADE, verbose_name="Вид характеристики")
    name = models.CharField(max_length=250, verbose_name='Название')

    def __str__(self):
        return f"{self.name}"
    
class Well(models.Model):
    """Скважина"""

    class Meta:
        db_table = 'wells'
        verbose_name = 'Скважина'
        verbose_name_plural = 'Скважины'

    name = models.CharField(max_length=250, verbose_name='Название')
    
    def __str__(self):
        return f"{self.name}"
    
class WellCharacteristicBinding(models.Model):
    """Привязка характеристик к скважине"""

    class Meta:
        db_table = 'wells_characteristics'
        verbose_name = 'Характеристика скважины'
        verbose_name_plural = 'Характеристики скважин'

    well = models.ForeignKey(Well, on_delete=models.CASCADE, verbose_name='Скважина')  # Используем абстрактную модель Well
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE, verbose_name='Характеристика')

    def __str__(self):
        return f"{self.well} - {self.characteristic}"
    
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