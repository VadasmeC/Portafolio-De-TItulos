from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import PersonasPerfiles
from notas.models import Notas

@receiver(post_save, sender=PersonasPerfiles)
def create_marks(sender, instance, created, **kwargs):
    if created:
        Notas.objects.create(
            NOTA_PEPE_ID=instance.PEPE_PERS_ID,  # Estudiante
            NOTA_CURS_ID=instance.PEPE_CURS_ID,  # Curso
            NOTA_VALOR1=None,
            NOTA_VALOR2=None,
            NOTA_VALOR3=None,
            NOTA_VALOR4=None,
            NOTA_VALOR5=None,
            average=None
        )
