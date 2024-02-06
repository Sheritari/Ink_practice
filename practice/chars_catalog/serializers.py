from rest_framework import serializers
from .models import CharacteristicType, Characteristic, Well, WellCharacteristicBinding

class CharacteristicTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacteristicType
        fields = '__all__'

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'

class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = '__all__'  

class WellCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellCharacteristicBinding
        fields = '__all__'