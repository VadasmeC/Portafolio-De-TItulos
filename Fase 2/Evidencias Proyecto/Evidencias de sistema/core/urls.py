
from django.urls import path
from .views import home, registro, exit, crear_persona_perfil, crear_publicacion, ver_publicaciones, ver_asignaturas, poner_nota, ver_notas_asignatura, editar_nota, registrar_asistencia, ver_asistencia,editar_asistencia, editar_publicacion,perfil, ver_notas_estudiante, listar_alumnos_por_asignatura, agregar_anotacion, get_alumnos_por_curso, ver_alumnos_a_cargo, crear_anotacion_tipo, crear_asignatura,crear_curso, crear_tipo_publicacion, agregar_comentario

urlpatterns = [
    path('', home, name='home'),
    path('crear_persona_perfil/', crear_persona_perfil, name='crear_persona_perfil'),
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/perfil_estudiante/', ver_notas_estudiante, name='ver_notas_estudiante'),
    path('logout/', exit, name='exit'),
    path('crear-publicacion/', crear_publicacion, name='crear publicacion'),
    path('muro/', ver_publicaciones, name='muro'),
    path('muro/editar/<int:publicacion_id>/', editar_publicacion, name='editar_publicacion'),
    path('ver_asignaturas/', ver_asignaturas, name='index_profesor'),
    path('crear_nota/<id>', poner_nota, name='poner_nota'),
    path('notas/asignatura/<int:asignatura_id>/', ver_notas_asignatura, name='ver_notas_asignatura'),
    path('editar-nota/<int:nota_id>/', editar_nota, name='editar_nota'),
    path('asistencia/registrar/<int:asignatura_id>/', registrar_asistencia, name='registrar_asistencia'),
    path('asistencia/asignatura/<int:asignatura_id>/', ver_asistencia, name='ver_asistencia'),
    path('asistencia/editar/<int:asistencia_id>/', editar_asistencia, name='editar_asistencia'),
    path('anotaciones/asignatura/<int:asignatura_id>/',listar_alumnos_por_asignatura, name='anotaciones_por_asignatura'),
    path('anotaciones/asignatura/<int:asignatura_id>/alumno/<int:alumno_id>/agregar/',agregar_anotacion, name='agregar_anotacion'),
    path('get-alumnos-por-curso/<int:curso_id>/', get_alumnos_por_curso, name='get_alumnos_por_curso'),
    path('perfil/perfil_apoderado/', ver_alumnos_a_cargo, name='ver_alumnos_a_cargo'),
    path('crear-curso/', crear_curso, name='crear_curso'),
    path('crear-asignatura/', crear_asignatura, name='crear_asignatura'),
    path('crear-anotacion-tipo/', crear_anotacion_tipo, name='crear_anotacion_tipo'),
    path('crear-tipo-publicacion/', crear_tipo_publicacion, name='crear_tipo_publicacion'),
    path('publicacion/<int:publicacion_id>/comentar/', agregar_comentario, name='agregar_comentario'),
    

]