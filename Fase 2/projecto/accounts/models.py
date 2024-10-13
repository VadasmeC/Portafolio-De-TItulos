from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Personas(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personas')
	PERS_NOMBRECOMPLETO = models.CharField(max_length=60,null=True, blank=True,verbose_name='Pers_nombrecompleto')
	PERS_FECHANAC = models.DateField(max_length=9,null=True, blank=True,verbose_name='Pers_fechanac')
	PERS_RUT = models.CharField(max_length=9,null=True, blank=True,verbose_name='Pers_rut')
	PERS_TELEFONO= models.CharField(max_length=14,null=True, blank=True,verbose_name='Pers_telefono')
	PERS_DIRECCION = models.CharField(max_length=40,null=True, blank=True,verbose_name='Pers_direccion')

	class Meta:
		ordering = ['-id']

def crear_user_persona(sender, instance, created, **kwargs):
	if created:
		Personas.objects.create(user=instance)

def guardar_user_persona(sender, instance, **kwargs):
	instance.personas.save()

post_save.connect(crear_user_persona, sender=User)
post_save.connect(guardar_user_persona, sender=User)