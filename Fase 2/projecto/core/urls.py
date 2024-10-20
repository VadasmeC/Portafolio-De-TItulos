
from django.urls import path
from .views import home, test, registro, exit, crear_persona_perfil, crear_publicacion, ver_publicaciones, index_profesor, poner_nota, lista_notas

urlpatterns = [
    path('', home, name='home'),
    path('crear_persona_perfil/', crear_persona_perfil, name='test'),
    path('registro/', registro, name='registro'),
    path('logout/', exit, name='exit'),
    path('crear-publicacion/', crear_publicacion, name='crear publicacion'),
    path('muro/', ver_publicaciones, name='muro'),
    path('ver_asignaturas/', index_profesor, name='index_profesor'),
    path('crear_nota/<id>', poner_nota, name='poner_nota'),
    path('lista_notas/', lista_notas, name='lista_notas'),


]