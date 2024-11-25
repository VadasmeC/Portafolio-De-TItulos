from django.db import models
from accounts.models import PersonasPerfiles, Cursos, Asignaturas

# Create your models here.

class AnotacionesTipos(models.Model):
    ANOT_T_ID = models.AutoField(primary_key=True, verbose_name='Id de tipo')
    ANOT_T_NOMBRE = models.CharField(max_length=50, verbose_name='Nombre tipo anotación')

    def __str__(self):
        return self.ANOT_T_NOMBRE

    class Meta:
        verbose_name = 'tipo'
        verbose_name_plural = 'tipos'

class Anotaciones(models.Model):
    ANOT_ID = models.AutoField(primary_key=True)
    ANOT_TITULO = models.TextField(max_length=100, null=True, blank=True, verbose_name='Titulo anotación')
    ANOT_DESCRIPCION = models.TextField(max_length=255, null=True, blank=True, verbose_name='Descripción')
    ANOT_FECHACREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    # Relaciones
    ANOT_PEPE_ID = models.ForeignKey(PersonasPerfiles, on_delete=models.CASCADE, verbose_name='Alumno')
    ANOT_CURS_ID = models.ForeignKey(Cursos, on_delete=models.CASCADE, verbose_name='Curso')
    ANOT_ASIG_ID = models.ForeignKey(Asignaturas, on_delete=models.CASCADE,null=True, blank=True, verbose_name='Asignatura')
    ANOT_ANOT_T_ID = models.ForeignKey(AnotacionesTipos, on_delete=models.CASCADE,null=True, blank=True, verbose_name='Tipo de Anotación')

    class Meta:
        verbose_name = 'Anotación'
        verbose_name_plural = 'Anotaciones'
        ordering = ['-ANOT_FECHACREACION']

    def __str__(self):
        return self.ANOT_TITULO