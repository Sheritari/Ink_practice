from django.contrib import admin
from .models import CharacteristicType, Characteristic, WellCharacteristicBinding, Well, User

# Регистрация модели "Справочник типов характеристик" в админке
@admin.register(CharacteristicType)
class CharacteristicTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_value_x', 'max_value_y']

# Регистрация модели "Характеристика" в админке
@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['name', 'characteristic_type']

# Регистрация модели "Привязка характеристик к скважине" в админке
@admin.register(WellCharacteristicBinding)
class WellCharacteristicBindingAdmin(admin.ModelAdmin):
    list_display = ['well', 'characteristic']

# Регистрация модели "Скважина" в админке
@admin.register(Well)
class WellAdmin(admin.ModelAdmin):
    list_display = ['name']

# Регистрация модели "Пользователь" в админке
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'email']