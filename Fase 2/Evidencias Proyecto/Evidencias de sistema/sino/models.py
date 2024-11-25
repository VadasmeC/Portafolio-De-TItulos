from django.db import models

# Create your models here.

class Sino(models.Model):
    SINO_ID = models.IntegerField(primary_key=True)
    SINO_NOMBRE = models.CharField(max_length=25)
    SINO_ESTADO = models.CharField(max_length=25)

    def __str__(self):
        return self.SINO_NOMBRE
