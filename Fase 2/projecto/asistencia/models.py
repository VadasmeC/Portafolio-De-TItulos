from django.db import models
from sino.models import Sino
from accounts.models import Cursos, Asignaturas, PersonasPerfiles

# Create your models here.

class Asistencia(models.Model):
    ASIS_ID = models.AutoField(primary_key=True)
    ASIS_FECHA = models.DateField(auto_now_add=True)
    #relaciones
    ASIS_SINO_PRESENTACERTIFICADO = models.ForeignKey(Sino, on_delete=models.CASCADE, related_name='certificado')
    ASIS_SINO_PRESENTE = models.ForeignKey(Sino, on_delete=models.CASCADE, related_name='presente')
    ASIS_CURS_ID = models.ForeignKey(Cursos, on_delete=models.CASCADE)
    ASIS_PEPE_ID = models.ForeignKey(PersonasPerfiles, on_delete=models.CASCADE)
    ASIS_ASIG_ID = models.ForeignKey(Asignaturas, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ASIS_FECHA} - {self.ASIS_PEPE_ID}"
