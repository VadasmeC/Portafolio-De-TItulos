from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Personas(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personas')
	PERS_NOMBRECOMPLETO = models.CharField(max_length=60,null=True, blank=True,verbose_name='Nombre completo')
	PERS_FECHANAC = models.DateField(max_length=9,null=True, blank=True,verbose_name='Fecha nacimiento')
	PERS_RUT = models.CharField(max_length=9,null=True, blank=True,verbose_name='Rut')
	PERS_TELEFONO= models.CharField(max_length=14,null=True, blank=True,verbose_name='Telefono')
	PERS_DIRECCION = models.CharField(max_length=40,null=True, blank=True,verbose_name='Direccion')



	class Meta:
		ordering = ['-id']
	
	def __str__(self):
   		return self.PERS_NOMBRECOMPLETO


class Perfiles(models.Model):
	PERF_ID = models.AutoField(primary_key=True, verbose_name = 'Id de perfiles')
	PERF_NOMBRE = models.CharField(max_length = 50, verbose_name = 'Perfiles')

	def __str__(self):
		return self.PERF_NOMBRE


class Cursos(models.Model):
	CURS_ID = models.AutoField(primary_key=True, verbose_name = 'Id de curso')
	CURS_NOMBRE = models.CharField(max_length = 50, verbose_name = 'Nombre curso')
	CURS_SALA = models.IntegerField(verbose_name = 'Numero de sala')
	CURS_ANNO = models.IntegerField(verbose_name = 'Año de curso')


	def __str__(self):
		return self.CURS_NOMBRE


class PersonasPerfiles(models.Model):
	PEPE_ID = models.AutoField(primary_key=True)
	PEPE_FECHACREACION = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
	PEPE_PERF_ID = models.ForeignKey(Perfiles, on_delete=models.CASCADE, related_name='personas_perfiles')
	PEPE_PERS_ID = models.ForeignKey(Personas, on_delete=models.CASCADE, related_name='perfiles')
	PEPE_CURS_ID = models.ForeignKey(Cursos, on_delete=models.CASCADE,null=True, related_name='cursos')

	class Meta:
		verbose_name = 'Perfil de Persona'
		verbose_name_plural = 'Perfiles de Personas'
		ordering = ['PEPE_ID']  
	def __str__(self):
		return f'Perfil {self.PEPE_PERF_ID.PERF_NOMBRE} de {self.PEPE_PERS_ID.PERS_NOMBRECOMPLETO} curso {self.PEPE_CURS_ID.CURS_NOMBRE}'


