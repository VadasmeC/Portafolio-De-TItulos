from django.db import models
from accounts.models import PersonasPerfiles, Cursos, Asignaturas

# Create your models here.

class Notas(models.Model):
    NOTA_ID = models.AutoField(primary_key=True)
    NOTA_VALOR = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Nota')
    NOTA_FECHACREACION = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    NOTA_DESCRIPCION = models.TextField(max_length=255, null=True, blank=True, verbose_name='Descripción')
    # Relaciones
    NOTA_PEPE_ID = models.ForeignKey(PersonasPerfiles, on_delete=models.CASCADE, verbose_name='Alumno')
    NOTA_CURS_ID = models.ForeignKey(Cursos, on_delete=models.CASCADE, verbose_name='Curso')
    NOTA_ASIG_ID = models.ForeignKey(Asignaturas, on_delete=models.CASCADE,null=True, blank=True, verbose_name='Asignatura')

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-NOTA_FECHACREACION']

    def __str__(self):
        return f'Nota{self.NOTA_VALOR}'