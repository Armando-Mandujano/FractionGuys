from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Student)
admin.site.register(models.Profesor)
admin.site.register(models.Estudiante)
admin.site.register(models.Grupo)
admin.site.register(models.Pregunta)
