# Generated by Django 5.1.2 on 2024-10-18 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muro', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicacionestipos',
            options={'verbose_name': 'tipo', 'verbose_name_plural': 'tipos'},
        ),
        migrations.RenameField(
            model_name='publicaciones',
            old_name='PUBL_DESCRIPCIO',
            new_name='PUBL_DESCRIPCION',
        ),
    ]