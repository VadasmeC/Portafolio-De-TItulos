from django.db import models
from accounts.models import PersonasPerfiles

# Create your models here.

class PublicacionesTipos(models.Model):
    PUTI_ID = models.AutoField(primary_key=True, verbose_name='Id de tipo')
    PUTI_NOMBRE = models.CharField(max_length=50, verbose_name='Nombre tipo publicación')

    def __str__(self):
        return self.PUTI_NOMBRE
    
    class Meta:
        verbose_name = 'tipo'
        verbose_name_plural = 'tipos'


class Publicaciones(models.Model):
    PUBL_ID = models.AutoField(primary_key=True, verbose_name='Id de publicación')
    PUBL_TITULO = models.CharField(max_length=200, verbose_name='Título de la publicación')
    PUBL_DESCRIPCION = models.TextField(verbose_name='Descripción publicación')
    PUBL_IMAGEN = models.ImageField(upload_to='publicaciones/', null=True, blank=True, verbose_name='Imagen')
    PUBL_FECHACREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    # Relaciones
    PUBL_PUTI_ID = models.ForeignKey(PublicacionesTipos, on_delete=models.CASCADE, verbose_name='Tipo de publicación')
    PUBL_PEPE_ID = models.ForeignKey(PersonasPerfiles, on_delete=models.CASCADE, verbose_name='Autor')

    def __str__(self):
        return self.PUBL_TITULO

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-PUBL_FECHACREACION']

