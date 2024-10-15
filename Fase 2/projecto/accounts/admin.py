from django.contrib import admin

# Register your models here.

from .models import Personas, Perfiles,PersonasPerfiles, Cursos

# Register your models here.
admin.site.register(Personas)
admin.site.register(Perfiles)
admin.site.register(PersonasPerfiles)
admin.site.register(Cursos)


