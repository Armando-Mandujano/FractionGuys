# Generated by Django 4.2 on 2023-04-17 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_remove_profesor_id_grupo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profesor',
            name='id_profesor',
        ),
    ]
