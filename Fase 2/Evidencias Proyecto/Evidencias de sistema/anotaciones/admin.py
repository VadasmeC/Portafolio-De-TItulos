from django.contrib import admin

# Register your models here.

from .models import Anotaciones, AnotacionesTipos

admin.site.register(AnotacionesTipos)
admin.site.register(Anotaciones)