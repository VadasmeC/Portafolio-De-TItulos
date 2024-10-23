from django.db import models
from accounts.models import PersonasPerfiles, Cursos

# Create your models here.

# NOTAS
class Notas(models.Model):
    NOTA_PEPE_ID = models.ForeignKey(PersonasPerfiles, on_delete=models.CASCADE, verbose_name='Alumno')
    NOTA_CURS_ID = models.ForeignKey(Cursos, on_delete=models.CASCADE, verbose_name='Curso')

    NOTA_ID = models.AutoField(primary_key=True)
    NOTA_VALOR1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 1')
    NOTA_VALOR2 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 2')
    NOTA_VALOR3 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 3')
    NOTA_VALOR4 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 4')
    NOTA_VALOR5 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 5')
    NOTA_FECHACREACION = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')

    average = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='Promedio')

    def __str__(self):
        return str(self.NOTA_CURS_ID)

    # Calcular el promedio (llamo a una función)
    def calculate_average(self):
        notas = [self.NOTA_VALOR1, self.NOTA_VALOR2, self.NOTA_VALOR3 ,self.NOTA_VALOR4, self.NOTA_VALOR5]
        Notas_validas = [nota for nota in notas if nota is not None]
        if Notas_validas:
            return sum(Notas_validas) / len(Notas_validas)
        return None

    def save(self, *args, **kwargs):
        # Verifico si alguna nota cambio
        if self.NOTA_VALOR1 or self.NOTA_VALOR2 or self.NOTA_VALOR3 or self.NOTA_VALOR4 or self.NOTA_VALOR5:
            self.average = self.calculate_average()     # Calcular el promedio (llamo a una función)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
