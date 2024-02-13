import openpyxl
from django.http import HttpResponse
import json
from .models import Characteristic

def export_characteristics_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="characteristics.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Characteristics'

    # Названия полей модели
    fields = ['id', 'name', 'characteristic_type', 'value']

    # Названия колонок в Excel
    worksheet.append([Characteristic._meta.get_field(field).verbose_name for field in fields])

    # Запись данных модели в Excel
    for characteristic in Characteristic.objects.all():
        value_str = json.dumps(characteristic.value)  # Преобразование JSON-объекта в строку
        row_data = [
            characteristic.id,
            getattr(characteristic, 'name'),
            characteristic.characteristic_type.name,
            value_str
        ]
        worksheet.append(row_data)

    # Сохранение данных в HttpResponse
    workbook.save(response)
    return response