# Generated by Django 4.2 on 2023-04-18 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_pregunta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pregunta',
            old_name='respuesta_alumno',
            new_name='respuesta',
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='respuestas_correcta',
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='resultado',
        ),
    ]
