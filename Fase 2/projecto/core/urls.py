
from django.urls import path
from .views import home, test, registro, exit, crear_persona_perfil, crear_publicacion, ver_publicaciones, ver_asignaturas, poner_nota, lista_notas, ver_notas_asignatura, editar_nota, registrar_asistencia, ver_asistencia,editar_asistencia, editar_publicacion,perfil

urlpatterns = [
    path('', home, name='home'),
    path('crear_persona_perfil/', crear_persona_perfil, name='test'),
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
    path('logout/', exit, name='exit'),
    path('crear-publicacion/', crear_publicacion, name='crear publicacion'),
    path('muro/', ver_publicaciones, name='muro'),
    path('muro/editar/<int:publicacion_id>/', editar_publicacion, name='editar_publicacion'),
    path('ver_asignaturas/', ver_asignaturas, name='index_profesor'),
    path('crear_nota/<id>', poner_nota, name='poner_nota'),
    path('lista_notas/', lista_notas, name='lista_notas'),
    path('notas/asignatura/<int:asignatura_id>/', ver_notas_asignatura, name='ver_notas_asignatura'),
    path('editar-nota/<int:nota_id>/', editar_nota, name='editar_nota'),
    path('asistencia/registrar/<int:asignatura_id>/', registrar_asistencia, name='registrar_asistencia'),
    path('asistencia/asignatura/<int:asignatura_id>/', ver_asistencia, name='ver_asistencia'),
    path('asistencia/editar/<int:asistencia_id>/', editar_asistencia, name='editar_asistencia'),


    

]