
from django.urls import path
from .views import home, test, registro, exit, crear_persona_perfil, crear_publicacion, ver_publicaciones, ver_asignaturas,PonerNotas,UpdateNota

urlpatterns = [
    path('', home, name='home'),
    path('crear_persona_perfil/', crear_persona_perfil, name='test'),
    path('registro/', registro, name='registro'),
    path('logout/', exit, name='exit'),
    path('crear-publicacion/', crear_publicacion, name='crear publicacion'),
    path('muro/', ver_publicaciones, name='muro'),
    path('ver_asignaturas/', ver_asignaturas, name='index_profesor'),
    path('poner_nota/', PonerNotas.as_view(), name='poner_nota'),
    path('update_nota/<id>', UpdateNota.as_view(), name='update_nota'),




]