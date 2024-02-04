from django.db import models
from jsonfield import JSONField

class CharacteristicType(models.Model):
    """Справочник типов характеристик"""

    class Meta:
        db_table = 'characteristic_types'
        verbose_name = 'Типы характеристик'
        verbose_name_plural = 'Типы характеристик'

    name = models.CharField(max_length=250, unique=True, verbose_name='Название')
    max_value_x = models.PositiveIntegerField(verbose_name='Максимальное значение по оси x')
    max_value_y = models.PositiveIntegerField(verbose_name='Максимальное значение по оси y')
    json_key_name = models.CharField(max_length=250, verbose_name='Название ключа в поле json')
    json_value_name = models.CharField(max_length=250, verbose_name='Название значения в поле json')

    def __str__(self):
        return f"{self.name} {self.max_value_x} {self.max_value_y} {self.json_key_name} {self.json_value_name}"
    
class Characteristic(models.Model):
    """Характеристика"""

    class Meta:
        db_table = 'characteristics'
        verbose_name = 'Описание характеристики'
        verbose_name_plural = 'Описание характеристики'

    value = JSONField(verbose_name="Значение")
    characteristic_type = models.ForeignKey(CharacteristicType, on_delete=models.CASCADE, verbose_name="Вид характеристики")
    name = models.CharField(max_length=250, verbose_name='Название')

    def __str__(self):
        return f"{self.value} {self.characteristic_type} {self.name}"
    
class Well(models.Model):
    """Скважина"""

    class Meta:
        abstract = True
        db_table = 'wells'
        verbose_name = 'Описание скважины'
        verbose_name_plural = 'Описание скважины'

    name = models.CharField(max_length=250, verbose_name='Название')
    
    def __str__(self):
        return f"{self.name}"
    
class WellCharacteristicBinding(models.Model):
    """Привязка характеристик к скважине"""

    well = models.ForeignKey(Well, on_delete=models.CASCADE)  # Используем абстрактную модель Well
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.well} - {self.characteristic}"

