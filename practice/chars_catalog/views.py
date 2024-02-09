from django.shortcuts import render
from rest_framework import viewsets
from .models import CharacteristicType, Characteristic, Well, WellCharacteristicBinding
from .serializers import CharacteristicTypeSerializer, CharacteristicSerializer, WellSerializer, WellCharacteristicSerializer
from .permissions import IsAdminOrReadOnly

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