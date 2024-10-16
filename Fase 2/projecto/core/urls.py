
from django.urls import path
from .views import home, test, registro, exit, crear_persona_perfil

urlpatterns = [
    path('', home, name='home'),
    path('crear_persona_perfil/', crear_persona_perfil, name='test'),
    path('registro/', registro, name='registro'),
    path('logout/', exit, name='exit'),
]