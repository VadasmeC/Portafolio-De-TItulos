from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, PersonasPerfilesForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


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
