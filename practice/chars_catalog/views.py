from django.shortcuts import render
from rest_framework import viewsets
from .models import CharacteristicType, Characteristic, Well, WellCharacteristicBinding
from .serializers import CharacteristicTypeSerializer, CharacteristicSerializer, WellSerializer, WellCharacteristicSerializer

class CharacteristicTypeViewSet(viewsets.ModelViewSet):
    queryset = CharacteristicType.objects.all()
    serializer_class = CharacteristicTypeSerializer

class CharacteristicViewSet(viewsets.ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer

class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer

class WellCharacteristicViewSet(viewsets.ModelViewSet):
    queryset = WellCharacteristicBinding.objects.all()
    serializer_class = WellCharacteristicSerializer