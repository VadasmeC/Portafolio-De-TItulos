# Generated by Django 5.1.2 on 2024-10-26 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sino',
            fields=[
                ('SINO_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('SINO_NOMBRE', models.CharField(max_length=10)),
                ('SINO_ESTADO', models.CharField(max_length=25)),
            ],
        ),
    ]