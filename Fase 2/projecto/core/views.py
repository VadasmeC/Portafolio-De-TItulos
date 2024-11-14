from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django.http import JsonResponse
from .forms import CustomUserCreationForm, PersonasPerfilesForm, PublicacionForm, NotasForm, NotaEditForm, AsistenciaEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from accounts.models import Personas, Perfiles
from django.contrib import messages
from accounts.models import Asignaturas, Perfiles, Cursos
from muro.models import Publicaciones, PersonasPerfiles
from notas.models import Notas
from sino.models import Sino
from asistencia.models import Asistencia
from collections import defaultdict




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
def test(request):
    return render(request, 'core/test.html')


@login_required
def perfil(request):
    perfiles_con_cursos = defaultdict(list)
    es_profesor = False
    es_alumno = False
    asignaturas_estudiante = []  # Para almacenar las asignaturas del estudiante

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

            # Verificar si el perfil es de profesor o alumno
            if perfil.PEPE_PERF_ID.PERF_ID == 1:
                es_profesor = True
            
            if perfil.PEPE_PERF_ID.PERF_ID == 22:
                es_alumno = True
                # Obtener las asignaturas en las que está inscrito el alumno
                asignaturas_estudiante = Asignaturas.objects.filter(ASI_CURS_ID=perfil.PEPE_CURS_ID)

    # Convertir defaultdict a un diccionario estándar
    perfiles_con_cursos = dict(perfiles_con_cursos)

    context = {
        'perfiles_con_cursos': perfiles_con_cursos,
        'es_profesor': es_profesor,
        'es_alumno': es_alumno,
        'asignaturas_estudiante': asignaturas_estudiante,  # Pasar asignaturas
    }

    if request.method == 'POST':
        data = json.loads(request.body)
        perfil_id = data.get('perfil_id')
        curso_id = data.get('curso_id')

        # Guardar la selección en la sesión del usuario
        request.session['perfil_id'] = perfil_id
        request.session['curso_id'] = curso_id

        # Obtener el perfil seleccionado para determinar si es profesor o alumno
        try:
            perfil = persona.perfiles.get(PEPE_ID=perfil_id)
            perfil_tipo = None

            if perfil.PEPE_PERF_ID.PERF_ID == 1:
                perfil_tipo = 'Profesor'
            elif perfil.PEPE_PERF_ID.PERF_ID == 22:
                perfil_tipo = 'Alumno'

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
# vista para crear perfil persona
@login_required
def crear_persona_perfil(request):
    if request.method == 'POST':
        form = PersonasPerfilesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El perfil ha sido subido correctamente.')
            return redirect('test')  # Redirige a alguna página de éxito después de guardar
    else:
        form = PersonasPerfilesForm()

    return render(request, 'core/test.html', {'form': form})
# vista para crear publicaciones
@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardamos el formulario pero no lo confirmamos aún (commit=False)
            publicacion = form.save(commit=False)
            # Obtener el perfil de la persona autenticada
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
    asignatura = Asignaturas.objects.get(ASI_ID=id)
    curso = asignatura.ASI_CURS_ID

    # Obtener los estudiantes del curso
    estudiantes = PersonasPerfiles.objects.filter(PEPE_CURS_ID=curso)

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
    }

    return render(request, 'notas/poner_nota.html', context)


#ver notas
def lista_notas(request):
    notas = Notas.objects.all()

    context = {
        'notas': notas,
    }
    return render(request, 'notas/lista_notas.html', context)




def ver_notas_asignatura(request, asignatura_id):
    asignatura = get_object_or_404(Asignaturas, ASI_ID=asignatura_id)

    # Obtener las notas asociadas al curso y asignatura por persona
    notas = Notas.objects.filter(
        NOTA_CURS_ID=asignatura.ASI_CURS_ID,
        NOTA_ASIG_ID=asignatura
    ).select_related('NOTA_PEPE_ID').order_by('NOTA_FECHACREACION')

    # Obtener estudiantes
    estudiantes = PersonasPerfiles.objects.filter(PEPE_CURS_ID=asignatura.ASI_CURS_ID)

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
    estudiantes = PersonasPerfiles.objects.filter(PEPE_CURS_ID=curso)

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

    # Obtener estudiantes del curso
    estudiantes = PersonasPerfiles.objects.filter(PEPE_CURS_ID=asignatura.ASI_CURS_ID)

    # Crear un diccionario de asistencias por estudiante
    asistencia_por_estudiante = {}
    fechas_unicas = sorted({asistencia.ASIS_FECHA for asistencia in asistencias})

    for estudiante in estudiantes:
        estudiante_id = estudiante.PEPE_ID
        asistencia_por_estudiante[estudiante_id] = {
            'total_asistencias': 0,
            'total_dias': len(fechas_unicas),  # Iniciar con el total de días igual al número de fechas únicas
            'asistencias': {}
        }
        
        # Inicializar cada fecha con una asistencia "ausente" por defecto
        for fecha in fechas_unicas:
            asistencia_por_estudiante[estudiante_id]['asistencias'][fecha] = None  # Esto indica "N/A" en el template si no hay asistencia real

    # Rellenar las asistencias reales
    for asistencia in asistencias:
        estudiante_id = asistencia.ASIS_PEPE_ID.PEPE_ID
        fecha = asistencia.ASIS_FECHA
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

#En trabajo
@login_required
def ver_notas_estudiante(request):
    # Obtener el perfil de estudiante autenticado
    estudiante = PersonasPerfiles.objects.get(PEPE_PERS_ID=request.user.personas, PEPE_PERF_ID=22)
    
    # Obtener las asignaturas en las que está inscrito el estudiante
    asignaturas = Asignaturas.objects.filter(ASI_CURS_ID=estudiante.PEPE_CURS_ID)

    # Obtener las notas del estudiante para cada asignatura
    notas = {}
    for asignatura in asignaturas:
        notas[asignatura] = Notas.objects.filter(NOTA_PEPE_ID=estudiante.PEPE_ID, NOTA_ASIG_ID=asignatura)

    # Calcular el promedio para cada asignatura
    promedios = {}
    for asignatura, notas_asignatura in notas.items():
        if notas_asignatura.exists():
            promedio = sum(nota.NOTA_VALOR for nota in notas_asignatura) / len(notas_asignatura)
        else:
            promedio = 0  # O el valor que desees mostrar si no hay notas
        promedios[asignatura] = promedio

    context = {
        'estudiante': estudiante,
        'asignaturas': asignaturas,
        'notas': notas,
        'promedios': promedios,
    }


    return render(request, 'core/perfil_estudiante.html', context)