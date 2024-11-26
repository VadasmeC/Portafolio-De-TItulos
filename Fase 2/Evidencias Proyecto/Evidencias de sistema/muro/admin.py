from django.contrib import admin

# Register your models here.

from .models import Publicaciones, PublicacionesTipos

# Register your models here.
admin.site.register(Publicaciones)
admin.site.register(PublicacionesTipos)