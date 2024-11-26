# Generated by Django 5.1.2 on 2024-10-19 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_personas_pers_direccion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personasperfiles',
            name='PEPE_PEPE_RESPONSABLE',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.personasperfiles', verbose_name='Responsable'),
        ),
        migrations.CreateModel(
            name='Asignaturas',
            fields=[
                ('ASI_ID', models.AutoField(primary_key=True, serialize=False)),
                ('ASI_NOMBRE', models.CharField(max_length=100, verbose_name='Nombre de la Asignatura')),
                ('ASI_CURS_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.cursos', verbose_name='Curso')),
            ],
            options={
                'verbose_name': 'Asignatura',
                'verbose_name_plural': 'Asignaturas',
                'ordering': ['ASI_NOMBRE'],
            },
        ),
    ]