from django.urls import path, include
from .views import CharacteristicTypeViewSet, CharacteristicViewSet, WellViewSet, WellCharacteristicViewSet
from .administration import RegisterView, LoginView, UserView, LogoutView
from rest_framework import routers
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from .export import export_characteristics_to_excel

router = routers.DefaultRouter()

router.register(r'chartype', CharacteristicTypeViewSet)
router.register(r'char', CharacteristicViewSet)
router.register(r'well', WellViewSet)
router.register(r'wellchar', WellCharacteristicViewSet)

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'), 
    path('schema/docs', SpectacularSwaggerView.as_view(url_name='schema')), 
    path('export_char_xlsx/', export_characteristics_to_excel, name='export_char'),
    path('', include(router.urls)),
]