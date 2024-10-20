from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, PersonasPerfilesForm, PublicacionForm, NotasForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from accounts.models import Personas, Perfiles
from django.contrib import messages
from accounts.models import Asignaturas, Perfiles, Cursos
from muro.models import Publicaciones, PersonasPerfiles
from notas.models import Notas



# Create your views here.

def home(request):
    return render(request, 'core/home.html')

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
def index_profesor(request):
    # Obtener el perfil del usuario logueado
    try:
        perfil_usuario = request.user.personas.perfiles.first()
    except PersonasPerfiles.DoesNotExist:
        perfil_usuario = None

    # Verificar si el usuario tiene el perfil de "profesor"
    perfil_profesor = Perfiles.objects.get(PERF_NOMBRE='Profesor')
    if perfil_usuario.PEPE_PERF_ID != perfil_profesor:
        return redirect('no_autorizado')  # Redirigir si no es profesor

    # Obtener los cursos asociados al profesor
    if perfil_usuario:
        cursos_asociados = Cursos.objects.filter(cursos=perfil_usuario)
    else:
        cursos_asociados = []
        
    if request.method == 'POST':
        asignaturas = Asignaturas.objects.filter()      # Lógica para agregar notas a cada estudiante del curso y asignatura seleccionados
    else:
        asignaturas = None

    context = {
        'cursos_asociados': cursos_asociados,
        'asignaturas': asignaturas,
    }

    return render(request, 'notas/index_profesor.html', context)


@login_required
def poner_nota(request, id):
    
    asignatura = Asignaturas.objects.get(ASI_NOMBRE = id)
    curso = asignatura.ASI_CURS_ID

    # Obtener los estudiantes del curso
    estudiantes = PersonasPerfiles.objects.filter(PEPE_CURS_ID=curso)

    if request.method == 'POST':
        # Guardar las notas enviadas por el formulario
        for estudiante in estudiantes:
            valor_nota = request.POST.get(f'nota_{estudiante.PEPE_ID}')  # Asegúrate de usar la clave correcta
            descripcion_nota = request.POST.get(f'descripcion_{estudiante.PEPE_ID}')  # Asegúrate de usar la clave correcta
            if valor_nota:
                nota = Notas(
                    NOTA_VALOR=valor_nota,
                    NOTA_DESCRIPCION=descripcion_nota,
                    NOTA_PEPE_ID=estudiante,  # Asegúrate de que este campo sea una instancia de PersonasPerfiles
                    NOTA_CURS_ID=curso  # Asegúrate de que este campo sea una instancia de Cursos
                )
                nota.save()
                messages.success(request, 'Se ha subido las notas.')
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
