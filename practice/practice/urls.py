from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from chars_catalog.views import CharacteristicTypeViewSet, CharacteristicViewSet, WellViewSet, WellCharacteristicViewSet

router = routers.SimpleRouter()

router.register(r'chartype', CharacteristicTypeViewSet)
router.register(r'char', CharacteristicViewSet)
router.register(r'well', WellViewSet)
router.register(r'wellchar', WellCharacteristicViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
