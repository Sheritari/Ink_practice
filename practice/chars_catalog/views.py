from django.shortcuts import render
from rest_framework import viewsets
from .models import CharacteristicType, Characteristic, Well, WellCharacteristicBinding
from .serializers import CharacteristicTypeSerializer, CharacteristicSerializer, WellSerializer, WellCharacteristicSerializer
from .permissions import IsAdminOrReadOnly
from .tasks import export_task
from os import remove
from django.http import HttpResponse
from celery.result import AsyncResult
from time import sleep

class CharacteristicTypeViewSet(viewsets.ModelViewSet):
    queryset = CharacteristicType.objects.all()
    serializer_class = CharacteristicTypeSerializer
    
    permission_classes = [IsAdminOrReadOnly]

class CharacteristicViewSet(viewsets.ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer

    permission_classes = [IsAdminOrReadOnly]

class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer

    permission_classes = [IsAdminOrReadOnly]  

class WellCharacteristicViewSet(viewsets.ModelViewSet):
    queryset = WellCharacteristicBinding.objects.all()
    serializer_class = WellCharacteristicSerializer   

    permission_classes = [IsAdminOrReadOnly]

def async_export_char(request):
    task = export_task.delay()
    task_result = task.get()

    file_path = None
    # Ждем, пока задача завершится и вернет путь к файлу
    if task_result:
        file_path = task_result

    if file_path:
        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as file:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        response = HttpResponse(file_iterator(file_path))
        response['Content-Disposition'] = f'attachment; filename="characteristics.xlsx'

        # Удаление файла с сервера после скачивания
        remove(file_path)

        return response
    else:
        return HttpResponse('File export in progress. Please try again later.')