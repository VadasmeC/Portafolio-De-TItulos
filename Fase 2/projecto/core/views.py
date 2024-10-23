from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.http import JsonResponse
from .forms import CustomUserCreationForm, PersonasPerfilesForm, PublicacionForm
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


# notas marks
# MOSTRAR LISTA DE ALUMNOS Y NOTAS A LOS PROFESORES
#PENDIENTE, NO JUNFIONA
class PonerNotas(TemplateView):
    template_name = 'poner_notas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        curso_id = request.session.get('curso_id')
        curso = Cursos.objects.get(CURS_NOMBRE=curso_id)
        
        # Obtiene el curso correspondiente
        curso = get_object_or_404(Cursos, CURS_NOMBRE=curso_id)
        
        # Filtra las notas correspondientes a ese curso
        notas = Notas.objects.filter(NOTA_CURS_ID=curso)

        student_data = []
        for nota in notas:
            # Obtiene el estudiante a partir del ForeignKey
            student = get_object_or_404(User, id=nota.NOTA_PEPE_ID.PEPE_ID)  # Asumimos que `id` es el atributo que identifica al usuario
            student_data.append({
                'mark_id': nota.NOTA_ID,
                'name': student.get_full_name(),
                'mark_1': nota.NOTA_VALOR1,
                'mark_2': nota.NOTA_VALOR2,
                'mark_3': nota.NOTA_VALOR3,
                'mark_4': nota.NOTA_VALOR4,
                'mark_5': nota.NOTA_VALOR5,
                'average': nota.average,
            })
        
        context['curso'] = curso
        context['student_data'] = student_data
        return context

# Actualizar notas de alumnos
class UpdateNota(UpdateView):
    model = Notas
    fields = ['NOTA_VALOR1', 'NOTA_VALOR2', 'NOTA_VALOR3', 'NOTA_VALOR4', 'NOTA_VALOR5']
    template_name = 'UpdateNota.html'

    def get_success_url(self):
        return reverse_lazy('poner_notas', kwargs={'curso_id': self.object.NOTA_CURS_ID.CURS_ID})

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nota = self.get_object()
        context['curso'] = nota.NOTA_CURS_ID.CURS_NOMBRE  # Asegúrate de que este es el campo que deseas mostrar
        context['nombre_estudiante'] = nota.NOTA_PEPE_ID.personas.get_full_name()  # Asegúrate de que 'personas' esté correcto
        return context

    def get_object(self, queryset=None):
        mark_id = self.kwargs['mark_id']
        return get_object_or_404(Notas, id=mark_id)