from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Personas, PersonasPerfiles
from muro.models import Publicaciones
from notas.models import Notas

#Formulario registro de personas
class CustomUserCreationForm(UserCreationForm):
    PERS_RUT = forms.CharField(max_length=9, required=True, label="RUT")
    PERS_NOMBRECOMPLETO = forms.CharField(max_length=60, required=True, label="Nombre Completo")
    PERS_TELEFONO = forms.CharField(max_length=14, required=True, label="Teléfono")
    PERS_FECHANAC = forms.DateField(required=True,label='Pers_fechanac')
    PERS_DIRECCION = forms.CharField(max_length=40,required=True,label='Pers_direccion')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    # Sobrescribimos el método save para guardar también en Personas
    def save(self, commit=True):
        user = super().save(commit=False)  # Primero guardamos el usuario
        if commit:
            user.save()
            # Creamos una instancia de Personas asociada al usuario
            Personas.objects.create(
                user=user,
                PERS_RUT=self.cleaned_data.get('PERS_RUT'),
                PERS_NOMBRECOMPLETO=self.cleaned_data.get('PERS_NOMBRECOMPLETO'),
                PERS_TELEFONO=self.cleaned_data.get('PERS_TELEFONO'),
                PERS_FECHANAC=self.cleaned_data.get('PERS_FECHANAC'),
                PERS_DIRECCION=self.cleaned_data.get('PERS_DIRECCION'),
            )
        return user
    

#Formulario personas_perfiles

class PersonasPerfilesForm(forms.ModelForm):

    class Meta:
        model = PersonasPerfiles
        fields = ['PEPE_PERS_ID', 'PEPE_CURS_ID','PEPE_PERF_ID', 'PEPE_PEPE_RESPONSABLE']


#Formulario publicaciones

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['PUBL_TITULO', 'PUBL_DESCRIPCION', 'PUBL_PUTI_ID', 'PUBL_IMAGEN']
        widgets = {
            'PUBL_FECHACREACION': forms.DateInput(attrs={'type': 'date'}),
        }
    #IMG opcional
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['PUBL_IMAGEN'].required = False

#Formulario notas
class NotasForm(forms.ModelForm):
    class Meta:
        model = Notas
        fields = ['NOTA_VALOR', 'NOTA_DESCRIPCION']
        widgets = {
            'NOTA_VALOR': forms.NumberInput(attrs={'min': 1, 'max': 7}),
            'NOTA_DESCRIPCION': forms.Textarea(attrs={'rows': 3}),
        }


