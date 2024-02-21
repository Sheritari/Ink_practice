from openpyxl import Workbook
from django.http import HttpResponse
from json import dumps
from .models import Characteristic
from os.path import join
from django.conf import settings

def export_characteristics_to_excel():
    file_path = join(settings.MEDIA_ROOT, 'characteristics.xlsx')  # Путь сохранения файла на сервере

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="characteristics.xlsx"'

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Characteristics'

    # Названия колонок в Excel
    column_names = [
        'id',
        Characteristic._meta.get_field('name').verbose_name,
        Characteristic._meta.get_field('characteristic_type').verbose_name,
        Characteristic._meta.get_field('value').verbose_name,
    ]
    worksheet.append(column_names)

    # Запись данных модели в Excel
    for characteristic in Characteristic.objects.all():
        value_str = dumps(characteristic.value)  # Преобразование JSON-объекта в строку
        row_data = [
            characteristic.id,
            getattr(characteristic, 'name'),
            characteristic.characteristic_type.name,
            value_str
        ]
        worksheet.append(row_data)

    # Сохранение данных в HttpResponse
    workbook.save(file_path)
    return file_path