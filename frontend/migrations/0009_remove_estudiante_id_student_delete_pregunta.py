# Generated by Django 4.2 on 2023-04-18 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_alter_profesor_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='id_student',
        ),
        migrations.DeleteModel(
            name='Pregunta',
        ),
    ]
