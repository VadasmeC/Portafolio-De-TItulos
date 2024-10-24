from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django.http import JsonResponse
from .forms import CustomUserCreationForm, PersonasPerfilesForm, PublicacionForm, NotasForm, NotaEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from accounts.models import Personas, Perfiles
from django.contrib import messages
from accounts.models import Asignaturas, Perfiles, Cursos
from muro.models import Publicaciones, PersonasPerfiles
from notas.models import Notas



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
            return redirect('crear publicacion')
    else:
        form = PublicacionForm()

    return render(request, 'muro/crear_publicacion.html', {'form': form})

#vista para ver publicaciones
@login_required
def ver_publicaciones(request):
    publicaciones = Publicaciones.objects.all().order_by('-PUBL_FECHACREACION')
    return render(request, 'muro/muro.html', {'publicaciones': publicaciones})

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
    # Obtener la asignatura
    asignatura = get_object_or_404(Asignaturas, ASI_ID=asignatura_id)

    # Obtener las notas asociadas al curso y asignatua por persona
    notas = Notas.objects.filter(
        NOTA_CURS_ID=asignatura.ASI_CURS_ID,  # Filtrar por curso
        NOTA_ASIG_ID=asignatura               # Filtrar por asignatura
    ).select_related('NOTA_PEPE_ID').order_by('NOTA_FECHACREACION')


    # Obtener estudiantes
    estudiantes = PersonasPerfiles.objects.filter(PEPE_CURS_ID=asignatura.ASI_CURS_ID)

    # Crear un diccionario de notas por estudiante
    notas_por_estudiante = {}
    for nota in notas:
        if nota.NOTA_PEPE_ID.PEPE_ID not in notas_por_estudiante:
            notas_por_estudiante[nota.NOTA_PEPE_ID.PEPE_ID] = []
        notas_por_estudiante[nota.NOTA_PEPE_ID.PEPE_ID].append(nota)

    # Determinar el máximo número de notas
    max_notas = max(len(notas) for notas in notas_por_estudiante.values()) if notas_por_estudiante else 0

    # Calculamos las celdas vacías para cada estudiante
    celdas_vacias_por_estudiante = {
        estudiante.PEPE_ID: max_notas - len(notas_por_estudiante.get(estudiante.PEPE_ID, []))
        for estudiante in estudiantes
    }

    context = {
        'asignatura': asignatura,
        'notas_por_estudiante': notas_por_estudiante,
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


