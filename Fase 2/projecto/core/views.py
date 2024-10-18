from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, PersonasPerfilesForm, PublicacionForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from muro.models import Publicaciones, PersonasPerfiles
from accounts.models import Personas



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
