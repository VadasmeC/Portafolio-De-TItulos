from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django.http import JsonResponse
from .forms import CustomUserCreationForm, PersonasPerfilesForm, PublicacionForm, NotasForm, NotaEditForm, AsistenciaEditForm, AnotacionForm, CursosForm, AsignaturasForm, AnotacionesTiposForm, PublicacionesTiposForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from accounts.models import Personas, Perfiles
from django.contrib import messages
from accounts.models import Asignaturas, Perfiles, Cursos
from muro.models import Publicaciones, PersonasPerfiles, Publicaciones_Comentarios
from notas.models import Notas
from sino.models import Sino
from asistencia.models import Asistencia
from collections import defaultdict

from anotaciones.models import Anotaciones

from django.core.mail import send_mail
from django.conf import settings



# Create your views here.

def home(request):
    # Verificar si el usuario tiene un perfil de Persona
    if hasattr(request.user, 'personas'):
        persona = request.user.personas
        # Obtener todos los perfiles de esa persona
        perfiles = persona.perfiles.all()
        
        # Para cada perfil, obtener el nombre del perfil y el curso asociado
        perfiles_con_curso = [(perfil.PEPE_ID, perfil.PEPE_PERF_ID.PERF_NOMBRE, perfil.PEPE_CURS_ID.CURS_NOMBRE) for perfil in perfiles]

    else:
        perfiles_con_curso = []

    context = {
        'perfiles_con_curso': perfiles_con_curso,
    }

    if request.method == 'POST':
        data = json.loads(request.body)
        perfil_id = data.get('perfil_id')
        curso_id = data.get('curso_id')

        # Guardar la selección en la sesión del usuario
        request.session['perfil_id'] = perfil_id
        request.session['curso_id'] = curso_id

        return JsonResponse({'success': True})
        
    return render(request, 'core/home.html', context)

@login_required
def crear_persona_perfil(request):
    if request.method == 'POST':
        form = PersonasPerfilesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil creado exitosamente.")
            return redirect('crear_persona_perfil')  # Redirige a la página deseada después de crear el perfil
        else:
            messages.error(request, "Hubo un error al crear el perfil.")
    else:
        form = PersonasPerfilesForm()

    context = {
        'form': form,
    }
    return render(request, 'core/crear_persona_perfil.html', context)


@login_required
def perfil(request):
    perfiles_con_cursos = defaultdict(list)
    es_profesor = False
    es_alumno = False
    es_apoderado = False
    es_admin = False
    asignaturas_estudiante = []  # Para almacenar las asignaturas del estudiante
    alumnos_a_cargo = []  # Para almacenar los alumnos a cargo del apoderado

    if hasattr(request.user, 'personas'):
        persona = request.user.personas
        perfiles = persona.perfiles.all()

        for perfil in perfiles:
            tipo_perfil = perfil.PEPE_PERF_ID.PERF_NOMBRE
            curso = perfil.PEPE_CURS_ID.CURS_NOMBRE if perfil.PEPE_CURS_ID else "Sin curso"
            perfil_id = perfil.PEPE_ID

            # Agrupar cursos por tipo de perfil
            perfiles_con_cursos[tipo_perfil].append({
                'perfil_id': perfil_id,
                'curso': curso,
            })

            # Verificar si el perfil es de profesor, alumno o apoderado
            if perfil.PEPE_PERF_ID.PERF_ID == 1:
                es_profesor = True
            
            if perfil.PEPE_PERF_ID.PERF_ID == 22:
                es_alumno = True
                # Obtener las asignaturas en las que está inscrito el alumno
                asignaturas_estudiante = Asignaturas.objects.filter(ASI_CURS_ID=perfil.PEPE_CURS_ID)

            if perfil.PEPE_PERF_ID.PERF_ID == 21:
                es_apoderado = True
                # Obtener los alumnos a cargo del apoderado
                if hasattr(perfil, 'PEPE_PEPE_RESPONSABLE') and perfil.PEPE_PEPE_RESPONSABLE:
                # Utiliza la instancia correcta de PersonasPerfiles para filtrar
                    alumnos_a_cargo = PersonasPerfiles.objects.filter(PEPE_PEPE_RESPONSABLE=perfil)
                else:
                    alumnos_a_cargo = []
            if perfil.PEPE_PERF_ID.PERF_ID == 23:
                es_profesor = True

    # Convertir defaultdict a un diccionario estándar
    perfiles_con_cursos = dict(perfiles_con_cursos)

    context = {
        'perfiles_con_cursos': perfiles_con_cursos,
        'es_profesor': es_profesor,
        'es_alumno': es_alumno,
        'es_apoderado': es_apoderado,
        'es_admin': es_admin,
        'asignaturas_estudiante': asignaturas_estudiante,
        'alumnos_a_cargo': alumnos_a_cargo,  # Pasar alumnos a cargo si es apoderado
    }

    if request.method == 'POST':
        data = json.loads(request.body)
        perfil_id = data.get('perfil_id')
        curso_id = data.get('curso_id')

        # Guardar la selección en la sesión del usuario
        request.session['perfil_id'] = perfil_id
        request.session['curso_id'] = curso_id

        # Obtener el perfil seleccionado para determinar si es profesor, alumno o apoderado
        try:
            perfil = persona.perfiles.get(PEPE_ID=perfil_id)
            perfil_tipo = None

            if perfil.PEPE_PERF_ID.PERF_ID == 1:
                perfil_tipo = 'Profesor'
            elif perfil.PEPE_PERF_ID.PERF_ID == 22:
                perfil_tipo = 'Alumno'
            elif perfil.PEPE_PERF_ID.PERF_ID == 21:
                perfil_tipo = 'Apoderado'
            elif perfil.PEPE_PERF_ID.PERF_ID == 23:
                perfil_tipo = 'Admin'    


            # Enviar el tipo de perfil en la respuesta JSON
            return JsonResponse({'success': True, 'perfil_tipo': perfil_tipo})

        except PersonasPerfiles.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Perfil no encontrado.'})

    return render(request, 'core/perfil.html', context)



def exit(request):
    logout(request)
    return redirect('home')

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        data["form"] = user_creation_form

    return render(request, 'registration/registro.html', data)

# vista para crear publicaciones
@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardamos el formulario pero no lo confirmamos aún (commit=False)
            publicacion = form.save(commit=False)
            # Obtener el perfil de la persona autenticada
            # Preparar la notificación por correo
            asunto = 'Nueva Publicación en el Sistema'
            mensaje = f'Se ha creado una nueva publicación: {publicacion.PUBL_TITULO}. Visita el sitio para más detalles.'

            # Obtener correos de los usuarios con un perfil apoderado
            apoderado_perfil_id = 21  
            correos_usuarios = [
                usuario.user.email
                for usuario in Personas.objects.filter(
                    id__in=PersonasPerfiles.objects.filter(PEPE_PERF_ID=apoderado_perfil_id).values_list('PEPE_PERS_ID', flat=True)
                )
                if usuario.user.email
            ]

            # Enviar la notificación
            enviar_notificacion_correo(asunto, mensaje, correos_usuarios)

            try:
                perfil = request.user.personas.perfiles.first()
                if perfil:
                    publicacion.PUBL_PEPE_ID = perfil  # Asignar el perfil encontrado
                else:
                    # Manejar caso donde el usuario no tiene perfil asociado
                    return redirect('crear publicacion')
            
            except PersonasPerfiles.DoesNotExist:
                return redirect('crear publicacion')
            form.save()
            messages.success(request, 'La publicacion se a subido correctamente.')
            return redirect('muro')
    else:
        form = PublicacionForm()

    return render(request, 'muro/crear_publicacion.html', {'form': form})

#vista para ver publicaciones
def ver_publicaciones(request):
    publicaciones = Publicaciones.objects.all().order_by('-PUBL_FECHACREACION')
    return render(request, 'muro/muro.html', {'publicaciones': publicaciones})

#editar publicaciones 
@login_required
def editar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicaciones, PUBL_ID=publicacion_id)

    # Asegurar que solo el autor pueda editar la publicación
    if request.user.personas.perfiles.first() != publicacion.PUBL_PEPE_ID:
        messages.error(request, "No tienes permiso para editar esta publicación.")
        return redirect('muro')

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            messages.success(request, "La publicación se ha actualizado correctamente.")
            return redirect('muro')
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'muro/editar_publicacion.html', {'form': form, 'publicacion': publicacion})

#vista para index_profesor
@login_required
def ver_asignaturas(request):
    curso_id = request.session.get('curso_id')
    curso = Cursos.objects.get(CURS_NOMBRE=curso_id)


    if curso_id:
        asignaturas = Asignaturas.objects.filter(ASI_CURS_ID=curso)
    else:
        asignaturas = []

    return render(request, 'notas/index_profesor.html', {'asignaturas': asignaturas})




@login_required
def poner_nota(request, id):
    asignatura = get_object_or_404(Asignaturas, ASI_ID=id)
    curso = asignatura.ASI_CURS_ID

    # Obtener solo los estudiantes (alumnos) del curso
    estudiantes = PersonasPerfiles.objects.filter(
        PEPE_CURS_ID=curso,
        PEPE_PERF_ID=22  # Solo alumnos
    )

    # Mensaje si no hay alumnos
    if not estudiantes:
        mensaje = "No hay estudiantes registrados en este curso."

    if request.method == 'POST':
        # Guardar las notas enviadas por el formulario
        for estudiante in estudiantes:
            valor_nota = request.POST.get(f'nota_{estudiante.PEPE_ID}')
            descripcion_nota = request.POST.get(f'descripcion_{estudiante.PEPE_ID}')
            if valor_nota:
                nota = Notas(
                    NOTA_VALOR=valor_nota,
                    NOTA_DESCRIPCION=descripcion_nota,
                    NOTA_PEPE_ID=estudiante,
                    NOTA_CURS_ID=curso,
                    NOTA_ASIG_ID=asignatura,
                )
                nota.save()
        return redirect('index_profesor')

    context = {
        'asignatura': asignatura,
        'curso': curso,
        'estudiantes': estudiantes,
        'mensaje': mensaje if not estudiantes else '',  # Mostrar mensaje si no hay estudiantes
    }

    return render(request, 'notas/poner_nota.html', context)


@login_required
def ver_notas_asignatura(request, asignatura_id):
    asignatura = get_object_or_404(Asignaturas, ASI_ID=asignatura_id)

    # Obtener las notas asociadas al curso y asignatura por persona
    notas = Notas.objects.filter(
        NOTA_CURS_ID=asignatura.ASI_CURS_ID,
        NOTA_ASIG_ID=asignatura
    ).select_related('NOTA_PEPE_ID').order_by('NOTA_FECHACREACION')

    # Obtener solo los estudiantes (alumnos) del curso
    estudiantes = PersonasPerfiles.objects.filter(
        PEPE_CURS_ID=asignatura.ASI_CURS_ID,
        PEPE_PERF_ID=22  # Solo alumnos
    )

    # Si no hay estudiantes, agregar mensaje
    if not estudiantes:
        mensaje = "No hay estudiantes registrados en este curso."

    # Crear un diccionario de notas y promedio por estudiante
    notas_por_estudiante = {}
    promedio_por_estudiante = {}

    for nota in notas:
        estudiante_id = nota.NOTA_PEPE_ID.PEPE_ID
        if estudiante_id not in notas_por_estudiante:
            notas_por_estudiante[estudiante_id] = []
        notas_por_estudiante[estudiante_id].append(nota)

    # Calcular el promedio de notas por estudiante
    for estudiante_id, notas in notas_por_estudiante.items():
        promedio_por_estudiante[estudiante_id] = sum(nota.NOTA_VALOR for nota in notas) / len(notas) if notas else 0

    # Determinar el máximo número de notas
    max_notas = max(len(notas) for notas in notas_por_estudiante.values()) if notas_por_estudiante else 0

    # Calcular celdas vacías para cada estudiante
    celdas_vacias_por_estudiante = {
        estudiante.PEPE_ID: max_notas - len(notas_por_estudiante.get(estudiante.PEPE_ID, []))
        for estudiante in estudiantes
    }

    context = {
        'asignatura': asignatura,
        'notas_por_estudiante': notas_por_estudiante,
        'promedio_por_estudiante': promedio_por_estudiante,
        'estudiantes': estudiantes,
        'max_notas': max_notas,
        'celdas_vacias_por_estudiante': celdas_vacias_por_estudiante,
        'mensaje': mensaje if not estudiantes else '',  # Añadir mensaje si no hay estudiantes
    }

    return render(request, 'notas/lista_notas.html', context)


#editar nota
@login_required
def editar_nota(request, nota_id):
    # Obtener la nota que se quiere editar
    nota = get_object_or_404(Notas, NOTA_ID=nota_id)

    if request.method == 'POST':
        # Crear un formulario con los datos enviados
        form = NotaEditForm(request.POST, instance=nota)

        if form.is_valid():
            form.save()
            messages.success(request, 'La nota ha sido actualizada exitosamente.')
            return redirect('ver_notas_asignatura', asignatura_id=nota.NOTA_ASIG_ID.ASI_ID)
    else:
        # Crear un formulario con los datos actuales de la nota
        form = NotaEditForm(instance=nota)

    context = {
        'form': form,
        'nota': nota,
    }

    return render(request, 'notas/editar_nota.html', context)

@login_required
def registrar_asistencia(request, asignatura_id):
    asignatura = Asignaturas.objects.get(ASI_ID=asignatura_id)
    curso = asignatura.ASI_CURS_ID
    # Filtrar solo los alumnos del curso
    estudiantes = PersonasPerfiles.objects.filter(
        PEPE_CURS_ID=curso,
        PEPE_PERF_ID=22  # 22 es el PERF_ID para 'Alumno'
    )

    if request.method == 'POST':
        # Opciones de presente/ausente
        presente_opcion = Sino.objects.get(SINO_ESTADO='True')
        ausente_opcion = Sino.objects.get(SINO_ESTADO='False')

        for estudiante in estudiantes:
            asistencia_valor = request.POST.get(f'asistencia_{estudiante.PEPE_ID}')
            certificado_valor = request.POST.get(f'certificado_{estudiante.PEPE_ID}', False)
            # Crear un nuevo registro de asistencia
            Asistencia.objects.create(
                ASIS_FECHA=request.POST.get('fecha'),
                ASIS_SINO_PRESENTE=presente_opcion if asistencia_valor == 'presente' else ausente_opcion,
                ASIS_SINO_PRESENTACERTIFICADO=presente_opcion if certificado_valor else ausente_opcion,
                ASIS_CURS_ID=curso,
                ASIS_PEPE_ID=estudiante,
                ASIS_ASIG_ID=asignatura,
            )
        
        return redirect('index_profesor')

    context = {
        'asignatura': asignatura,
        'curso': curso,
        'estudiantes': estudiantes,
    }
    return render(request, 'asistencia/registrar_asistencia.html', context)


def ver_asistencia(request, asignatura_id):
    # Obtener la asignatura
    asignatura = get_object_or_404(Asignaturas, ASI_ID=asignatura_id)

    # Obtener las asistencias asociadas al curso y asignatura
    asistencias = Asistencia.objects.filter(
        ASIS_CURS_ID=asignatura.ASI_CURS_ID,
        ASIS_ASIG_ID=asignatura
    ).select_related('ASIS_PEPE_ID', 'ASIS_SINO_PRESENTE')

    # Obtener solo los estudiantes (alumnos) del curso
    estudiantes = PersonasPerfiles.objects.filter(
        PEPE_CURS_ID=asignatura.ASI_CURS_ID,
        PEPE_PERF_ID=22  # Filtrar solo perfiles de tipo 'Alumno'
    )

    # Crear un diccionario de asistencias por estudiante
    asistencia_por_estudiante = {}
    fechas_unicas = sorted({asistencia.ASIS_FECHA for asistencia in asistencias})

    for estudiante in estudiantes:
        estudiante_id = estudiante.PEPE_ID
        # Inicializar cada estudiante en el diccionario con asistencias vacías
        asistencia_por_estudiante[estudiante_id] = {
            'total_asistencias': 0,
            'total_dias': len(fechas_unicas),  # Iniciar con el total de días igual al número de fechas únicas
            'asistencias': {fecha: None for fecha in fechas_unicas}  # Asistencia 'N/A' por defecto
        }

    # Rellenar las asistencias reales
    for asistencia in asistencias:
        estudiante_id = asistencia.ASIS_PEPE_ID.PEPE_ID
        fecha = asistencia.ASIS_FECHA
        # Verificar si el estudiante está en el diccionario antes de asignar
        if estudiante_id in asistencia_por_estudiante:
            asistencia_por_estudiante[estudiante_id]['asistencias'][fecha] = asistencia

            # Contar las asistencias
            if asistencia.ASIS_SINO_PRESENTE.SINO_ESTADO == "True":  # Verifica si el estudiante está presente
                asistencia_por_estudiante[estudiante_id]['total_asistencias'] += 1

    # Calcular el porcentaje de asistencia para cada estudiante
    for estudiante_id, datos in asistencia_por_estudiante.items():
        if datos['total_dias'] > 0:
            datos['porcentaje_asistencia'] = (datos['total_asistencias'] / datos['total_dias']) * 100
        else:
            datos['porcentaje_asistencia'] = 0  # Evitar división por cero

    context = {
        'asignatura': asignatura,
        'asistencia_por_estudiante': asistencia_por_estudiante,
        'estudiantes': estudiantes,
        'fechas_unicas': fechas_unicas,
    }

    return render(request, 'asistencia/ver_asistencia.html', context)



@login_required
def editar_asistencia(request, asistencia_id):
    # Obtener la asistencia que se quiere editar
    asistencia = get_object_or_404(Asistencia, ASIS_ID=asistencia_id)

    if request.method == 'POST':
        # Crear un formulario con los datos enviados
        form = AsistenciaEditForm(request.POST, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'La asistencia ha sido actualizada exitosamente.')
            return redirect('ver_asistencia', asignatura_id=asistencia.ASIS_ASIG_ID.ASI_ID)  # Redirigir a la vista de asistencia después de guardar
    else:
        # Crear un formulario con los datos actuales de la asistencia
        form = AsistenciaEditForm(instance=asistencia)

    context = {
        'form': form,
        'asistencia': asistencia,
    }

    return render(request, 'asistencia/editar_asistencia.html', context)

@login_required
def ver_notas_estudiante(request):
    # Obtener el perfil de estudiante autenticado
    estudiante = PersonasPerfiles.objects.get(PEPE_PERS_ID=request.user.personas, PEPE_PERF_ID=22)
    
    # Obtener las asignaturas en las que está inscrito el estudiante
    asignaturas = Asignaturas.objects.filter(ASI_CURS_ID=estudiante.PEPE_CURS_ID)

    # Crear un diccionario para almacenar notas, asistencia y anotaciones
    datos_por_asignatura = {}

    for asignatura in asignaturas:
        # Obtener notas para cada asignatura
        notas = Notas.objects.filter(NOTA_PEPE_ID=estudiante.PEPE_ID, NOTA_ASIG_ID=asignatura)
        if notas.exists():
            promedio = sum(nota.NOTA_VALOR for nota in notas) / len(notas)
        else:
            promedio = 0
        
        # Obtener asistencia para la asignatura actual
        asistencias = Asistencia.objects.filter(
            ASIS_CURS_ID=asignatura.ASI_CURS_ID,
            ASIS_ASIG_ID=asignatura
        )

        # Calcular las fechas únicas de las clases registradas para la asignatura
        fechas_unicas = sorted({asistencia.ASIS_FECHA for asistencia in asistencias})
        total_dias = len(fechas_unicas)  # Total de días únicos en los que hubo clases

        # Inicializar datos de asistencia
        total_asistencias = 0
        
        # Calcular asistencias reales, incluyendo N/A
        for fecha in fechas_unicas:
            asistencia = asistencias.filter(ASIS_FECHA=fecha, ASIS_PEPE_ID=estudiante.PEPE_ID).first()
            if asistencia and asistencia.ASIS_SINO_PRESENTE:
                if asistencia.ASIS_SINO_PRESENTE.SINO_ESTADO == "True":
                    total_asistencias += 1

        # Calcular el porcentaje de asistencia, incluyendo los N/A
        if total_dias > 0:
            porcentaje_asistencia = (total_asistencias / total_dias) * 100
        else:
            porcentaje_asistencia = 0  # Evitar división por cero

        # Obtener anotaciones relacionadas con el estudiante y la asignatura actual
        anotaciones = Anotaciones.objects.filter(
            ANOT_PEPE_ID=estudiante,
            ANOT_ASIG_ID=asignatura
        )

        # Almacenar la información en el diccionario
        datos_por_asignatura[asignatura] = {
            'notas': notas,
            'promedio': promedio,
            'total_clases': total_dias,
            'total_clases_asistidas': total_asistencias,
            'porcentaje_asistencia': round(porcentaje_asistencia, 2),
            'anotaciones': anotaciones,  # Añadir anotaciones al contexto
        }

    context = {
        'estudiante': estudiante,
        'datos_por_asignatura': datos_por_asignatura,
    }

    return render(request, 'core/perfil_estudiante.html', context)


@login_required
def listar_alumnos_por_asignatura(request, asignatura_id):
    # Obtener la asignatura específica
    asignatura = get_object_or_404(Asignaturas, ASI_ID=asignatura_id)
    
    # Filtrar estudiantes con el perfil "Alumno" (perfil con PERF_ID = 22)
    alumnos = PersonasPerfiles.objects.filter(
        PEPE_CURS_ID=asignatura.ASI_CURS_ID,
        PEPE_PERF_ID__PERF_ID=22
    )
    
    context = {
        'asignatura': asignatura,
        'alumnos': alumnos
    }
    
    return render(request, 'anotaciones/anotaciones.html', context)

@login_required
def agregar_anotacion(request, asignatura_id, alumno_id):
    asignatura = get_object_or_404(Asignaturas, ASI_ID=asignatura_id)
    alumno = get_object_or_404(PersonasPerfiles, PEPE_ID=alumno_id)

    if request.method == 'POST':
        form = AnotacionForm(request.POST)
        if form.is_valid():
            nueva_anotacion = form.save(commit=False)
            nueva_anotacion.ANOT_PEPE_ID = alumno  # Asignar automáticamente el alumno seleccionado
            nueva_anotacion.ANOT_CURS_ID = alumno.PEPE_CURS_ID  # También asignar el curso
            nueva_anotacion.ANOT_ASIG_ID = asignatura  # Asignar la asignatura
            nueva_anotacion.save()
            return redirect('anotaciones_por_asignatura', asignatura_id=asignatura_id)
    else:
        form = AnotacionForm()

    context = {
        'form': form,
        'alumno': alumno,
        'asignatura': asignatura,
    }
    return render(request, 'anotaciones/agregar_anotacion.html', context)

@login_required
def get_alumnos_por_curso(request, curso_id):
    # Obtener solo los perfiles de alumnos del curso seleccionado
    alumnos = PersonasPerfiles.objects.filter(
        PEPE_CURS_ID=curso_id,
        PEPE_PERF_ID__PERF_NOMBRE='Alumno'
    ).values('PEPE_ID', 'PEPE_PERS_ID__PERS_NOMBRECOMPLETO')
    
    # Crear una lista con los datos de los alumnos
    alumnos_list = list(alumnos)
    
    return JsonResponse(alumnos_list, safe=False)

@login_required
def ver_alumnos_a_cargo(request):
    # Obtener todos los perfiles del apoderado logueado
    perfiles_apoderado = PersonasPerfiles.objects.filter(
        PEPE_PERS_ID=request.user.personas,
        PEPE_PERF_ID__PERF_NOMBRE='Apoderado'
    )

    # Si el apoderado tiene al menos un perfil registrado
    if perfiles_apoderado.exists():
        alumnos_a_cargo = []

        # Buscar los alumnos a cargo en función de cada perfil de apoderado
        for perfil_apoderado in perfiles_apoderado:
            alumnos = PersonasPerfiles.objects.filter(
                PEPE_PEPE_RESPONSABLE=perfil_apoderado.PEPE_ID, 
                PEPE_PERF_ID__PERF_ID=22  # Filtrar solo los alumnos
            )
            alumnos_a_cargo.extend(alumnos)

        # Preparar la información organizada por asignatura para cada alumno
        alumnos_info = []
        for alumno in alumnos_a_cargo:
            # Obtener las asignaturas en las que está inscrito el alumno
            asignaturas = Asignaturas.objects.filter(ASI_CURS_ID=alumno.PEPE_CURS_ID)
            datos_por_asignatura = {}

            for asignatura in asignaturas:
                # Obtener notas para cada asignatura
                notas = Notas.objects.filter(NOTA_PEPE_ID=alumno.PEPE_ID, NOTA_ASIG_ID=asignatura)
                if notas.exists():
                    promedio = sum(nota.NOTA_VALOR for nota in notas) / len(notas)
                else:
                    promedio = 0
                
                # Obtener asistencia para la asignatura actual
                asistencias = Asistencia.objects.filter(
                    ASIS_CURS_ID=asignatura.ASI_CURS_ID,
                    ASIS_ASIG_ID=asignatura
                )

                # Calcular las fechas únicas de las clases registradas para la asignatura
                fechas_unicas = sorted({asistencia.ASIS_FECHA for asistencia in asistencias})
                total_dias = len(fechas_unicas)  # Total de días únicos en los que hubo clases

                # Inicializar datos de asistencia
                total_asistencias = 0
                
                # Calcular asistencias reales, incluyendo N/A
                for fecha in fechas_unicas:
                    asistencia = asistencias.filter(ASIS_FECHA=fecha, ASIS_PEPE_ID=alumno.PEPE_ID).first()
                    if asistencia and asistencia.ASIS_SINO_PRESENTE:
                        if asistencia.ASIS_SINO_PRESENTE.SINO_ESTADO == "True":
                            total_asistencias += 1

                # Calcular el porcentaje de asistencia, incluyendo los N/A
                if total_dias > 0:
                    porcentaje_asistencia = (total_asistencias / total_dias) * 100
                else:
                    porcentaje_asistencia = 0  # Evitar división por cero

                # Obtener anotaciones relacionadas con el alumno y la asignatura actual
                anotaciones = Anotaciones.objects.filter(
                    ANOT_PEPE_ID=alumno,
                    ANOT_ASIG_ID=asignatura
                )

                # Almacenar la información en el diccionario
                datos_por_asignatura[asignatura] = {
                    'notas': notas,
                    'promedio': round(promedio, 2),
                    'total_clases': total_dias,
                    'total_clases_asistidas': total_asistencias,
                    'porcentaje_asistencia': round(porcentaje_asistencia, 2),
                    'anotaciones': anotaciones,
                }

            # Agregar información del alumno al contexto
            alumnos_info.append({
                'alumno': alumno,
                'datos_por_asignatura': datos_por_asignatura,
            })

        context = {
            'alumnos_info': alumnos_info,
        }

        return render(request, 'core/ver_alumnos_a_cargo.html', context)

    else:
        # Si no es apoderado o no tiene perfiles, redirigir a su perfil
        return redirect('perfil')
    
@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige al perfil de admin después de guardar
    else:
        form = CursosForm()
    
    context = {'form': form}
    return render(request, 'core/formulario_curso.html', context)


@login_required
def crear_asignatura(request):
    if request.method == 'POST':
        form = AsignaturasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = AsignaturasForm()
    
    context = {'form': form}
    return render(request, 'core/formulario_asignatura.html', context)

@login_required
def crear_anotacion_tipo(request):
    if request.method == 'POST':
        form = AnotacionesTiposForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = AnotacionesTiposForm()
    
    context = {'form': form}
    return render(request, 'core/formulario_anotacion_tipo.html', context)

@login_required
def crear_tipo_publicacion(request):
    if request.method == 'POST':
        form = PublicacionesTiposForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de publicación creado con éxito.')
            return redirect('crear_tipo_publicacion')  # Redirigir a la página del perfil o donde prefieras
        else:
            messages.error(request, 'Hubo un error al crear el tipo de publicación.')
    else:
        form = PublicacionesTiposForm()
    
    return render(request, 'core/crear_tipo_publicacion.html', {'form': form})


def enviar_notificacion_correo(asunto, mensaje, destinatarios):
    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        destinatarios,
        fail_silently=False,
    )

@login_required
def agregar_comentario(request, publicacion_id):
    publicacion = get_object_or_404(Publicaciones, PUBL_ID=publicacion_id)
    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        perfil = request.user.personas.perfiles.first()  # Obtener el perfil del usuario autenticado
        if perfil and comentario_texto:
            comentario = Publicaciones_Comentarios.objects.create(
                PUCO_COMENTARIO=comentario_texto,
                PUCO_PUBL_ID=publicacion,
                PUCO_PEPE_ID=perfil
            )
            comentario.save()
            messages.success(request, "¡Comentario agregado!")
        else:
            messages.error(request, "No se pudo agregar el comentario.")
    return redirect('muro')