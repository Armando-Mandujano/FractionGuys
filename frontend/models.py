from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Student(models.Model):
    points = models.CharField(max_length=4)
    date = models.DateTimeField('date added')
    def __str__(self):
        return f"Date: {self.date},points: {self.points}points"

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Profesor(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(editable=False, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'grupo']

    def __str__(self):
        return self.nombre

    def has_perm(self, perm, obj=None):
        if self.is_staff:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_staff:
            return True
        return False


    
class Estudiante(models.Model):
    numero_de_lista = models.IntegerField()
    grupo = models.CharField(max_length=1)
    #id_grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.grupo} - {self.numero_de_lista}"


class Grupo(models.Model):
    numero_de_grupo = models.IntegerField(unique=True)
    id_grupo = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.numero_de_grupo)

class Pregunta(models.Model):
    #id_student = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    list_number = models.IntegerField()
    grupo = models.CharField(max_length=200)
    pregunta = models.CharField(max_length=200)
    respuesta = models.IntegerField()
    respuesta_alumno = models.IntegerField()
    nivel = models.CharField(max_length=255)
    dificultad = models.IntegerField()
    fecha = models.DateTimeField()
    tiempo_asignado = models.IntegerField()
    def __str__(self):
        return f"{self.pregunta}" 