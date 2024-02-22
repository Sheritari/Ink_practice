from django.test import TestCase
import unittest
from .views import CharacteristicTypeViewSet
from .models import CharacteristicType
from .serializers import CharacteristicTypeSerializer
from .permissions import TypeCharacteristicPermission
from django.db.models.query import QuerySet
from django.test import Client

class CharacteristicTypeViewSetTestCase(unittest.TestCase):
    
    def setUp(self):
        client = Client()

        # Создание данных для входа
        login_data = {
            'username': 'bl',
            'password': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        }

        # Отправка POST-запроса к маршруту для входа
        client.post('/api/v1/login', data=login_data)
        self.client = client

    def test_queryset(self):
        view = CharacteristicTypeViewSet()
        queryset = view.queryset

        # Проверяем, что queryset является экземпляром QuerySet
        self.assertIsInstance(queryset, QuerySet)

        # Проверяем, что queryset соответствует ожидаемой модели
        expected_queryset = CharacteristicType.objects.all()
        self.assertEqual(list(queryset), list(expected_queryset))

    def test_serializer_class(self):
        view = CharacteristicTypeViewSet()
        serializer_class = view.serializer_class
        self.assertEqual(serializer_class, CharacteristicTypeSerializer)

    def test_permission_classes(self):
        view = CharacteristicTypeViewSet()
        permission_classes = view.permission_classes
        self.assertIn(TypeCharacteristicPermission, permission_classes)

    def test_create_characteristic_type(self):
        data = {"name": "Test Characteristic", "max_value_x": 999, "max_value_y": 999, "json_key_name": "testkey", "json_value_name": "testvalue"}
        response = self.client.post('/api/v1/chartype/', data=data)
        self.assertEqual(response.status_code, 201)

        # Получаем объект CharacteristicType
        characteristic_type = CharacteristicType.objects.filter(id=response.json().get('id')).first()

        # Далее удаляем объект в конце теста
        characteristic_type.delete()

    def test_list_characteristic_types(self):
        response = self.client.get('/api/v1/chartype/')
        self.assertEqual(response.status_code, 200) 

if __name__ == '__main__':
    unittest.main()