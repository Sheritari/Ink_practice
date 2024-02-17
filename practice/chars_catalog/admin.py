from django.contrib import admin
from .models import CharacteristicType, Characteristic, WellCharacteristicBinding, Well, User
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

# Регистрация модели "Справочник типов характеристик" в админке
@admin.register(CharacteristicType)
class CharacteristicTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_value_x', 'max_value_y']

class CharacteristicResource(resources.ModelResource):
        class Meta:
            model = Characteristic
            
# Регистрация модели "Характеристика" в админке
@admin.register(Characteristic)
class CharacteristicAdmin(ImportExportActionModelAdmin):
    resource_class = CharacteristicResource
    list_display = ['name', 'characteristic_type']
    
#  class CharacteristicAdmin(admin.ModelAdmin):
#     list_display = ['name', 'characteristic_type']

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