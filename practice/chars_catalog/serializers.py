from rest_framework import serializers
from .models import CharacteristicType, Characteristic, Well, WellCharacteristicBinding, User

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance