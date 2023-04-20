from django.shortcuts import render
from django.http import JsonResponse
from .models import Student
from django.db.models import Max, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms
from .forms import RegisterUserForm
from .forms import ProfesorCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Pregunta, Estudiante
from datetime import timedelta
from django.utils import timezone
from random import randint
import json
import datetime
from django.db.models import Count, Sum
from django.urls import reverse
from django.views import View
from .forms import EstudianteForm

# Create your views here.
def homepage(request):
    return redirect('login')

from django.shortcuts import render, redirect, reverse
from django.db.models import Max
from random import randint
from .models import Pregunta, Student

def index(request):
    #maxp = Student.objects.all().aggregate(Max('points'))
    num_respuestas_uno = Pregunta.objects.filter(respuesta=1).count()
    num_respuestas_cero = Pregunta.objects.filter(respuesta=0).count()
    porcentaje = int(round((num_respuestas_uno/(num_respuestas_uno + num_respuestas_cero))*100))
    primer_registro = Pregunta.objects.order_by('fecha').first()
    ultimo_registro = Pregunta.objects.order_by('-fecha').first()
    diferencia = ultimo_registro.fecha - primer_registro.fecha
    dias_transcurridos = diferencia.days
    estudiantes = Pregunta.objects.values('list_number', 'grupo').distinct()
    data = [randint(0, 100) for _ in range(7)]

    url = reverse('student_results2', args=[1, 1])
    grupo = 1
    numero_lista = 1

    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        numero_lista = request.POST.get('numero_lista')
        url = reverse('student_results2', args=[numero_lista, grupo])

    ctx = {'maxp': num_respuestas_uno, 'maxp2': num_respuestas_cero, 'porcentaje': porcentaje, 'dias_transcurridos': dias_transcurridos, 'data': data, 'url': url, 'grupo': grupo, 'numero_lista': numero_lista}
    
    return render(request, "frontend/index.html", ctx)

def student_results(request):
    # Obtener todos los resultados
    results = Pregunta.objects.order_by('fecha')

    # Crear una lista para almacenar los resultados por periodo de 7 días
    data = []

    # Obtener la fecha del primer registro
    first_date = results.first().fecha.date()

    # Iterar sobre los registros en intervalos de 7 días
    while True:
        # Obtener la fecha final del periodo de 7 días
        end_date = first_date + timedelta(days=7)

        # Obtener los resultados del periodo de 7 días
        period_results = results.filter(fecha__gte=first_date, fecha__lt=end_date)

        # Obtener el número total de preguntas y el número de preguntas respondidas correctamente
        num_total = period_results.count()
        num_correct = period_results.filter(respuesta=1).count()

        # Calcular el porcentaje de aciertos
        if num_total > 0:
            percentage = round(num_correct / num_total * 100, 2)
        else:
            percentage = 0

        # Agregar el resultado a la lista
        period_str = f"{first_date}-{end_date}"
        data.append({"id": len(data) + 1, "points": str(percentage), "date": period_str})

        # Actualizar la fecha del primer registro al final del periodo de 7 días
        first_date = end_date

        # Terminar si no hay más registros después del final del último periodo de 7 días
        if not results.filter(fecha__gte=first_date):
            break

    # Devolver la lista como un objeto JSON
    return JsonResponse(data, safe=False)


def student_results2(request, list_number, grupo):
    # Obtener todos los resultados que coincidan con el list_number y el grupo dados
    results = Pregunta.objects.filter(list_number=list_number, grupo=grupo).order_by('fecha')

    # Crear una lista para almacenar los resultados por periodo de 7 días
    data = []

    # Obtener la fecha del primer registro
    first_date = results.first().fecha.date()

    # Iterar sobre los registros en intervalos de 7 días
    while True:
        # Obtener la fecha final del periodo de 7 días
        end_date = first_date + timedelta(days=7)

        # Obtener los resultados del periodo de 7 días
        period_results = results.filter(fecha__gte=first_date, fecha__lt=end_date)

        # Obtener el número total de preguntas y el número de preguntas respondidas correctamente
        num_total = period_results.count()
        num_correct = period_results.filter(respuesta=1).count()

        # Calcular el porcentaje de aciertos
        if num_total > 0:
            percentage = round(num_correct / num_total * 100, 2)
        else:
            percentage = 0

        # Agregar el resultado a la lista
        period_str = f"{first_date}-{end_date}"
        data.append({"id": len(data) + 1, "points": str(percentage), "date": period_str})

        # Actualizar la fecha del primer registro al final del periodo de 7 días
        first_date = end_date

        # Terminar si no hay más registros después del final del último periodo de 7 días
        if not results.filter(fecha__gte=first_date):
            break

    # Devolver la lista como un objeto JSON
    return JsonResponse(data, safe=False)

def aboutus(request):
    return render(request, "frontend/aboutus.html")



def chart(request):
    maxp_list = list(Estudiante.objects.values_list('numero_de_lista', flat=True))
    groupList = Estudiante.objects.all()
    ctx = {'maxp': max(maxp_list), 'groupList': groupList}
    return render(request, 'frontend/chart.html', ctx)

def delete_student(request, id):
    student = Estudiante.objects.get(id=id)
    groupList = Estudiante.objects.filter(numero_de_lista=student.numero_de_lista, grupo=student.grupo)
    groupList.delete()
    preguntaList = Pregunta.objects.filter(list_number=student.numero_de_lista, grupo=student.grupo)
    preguntaList.delete()
    return redirect('chart')


def crear_estudiante(request):
    if request.method == 'POST':
        grupo = request.POST['grupo']
        numero_de_lista = request.POST['numero_de_lista']
        
        # Verificar si ya existe un estudiante con ese grupo y número de lista
        if Estudiante.objects.filter(grupo=grupo, numero_de_lista=numero_de_lista).exists():
            messages.error(request, 'Ya existe un estudiante con ese grupo y número de lista')
            return redirect('chart')
        
        # Crear el nuevo estudiante
        estudiante = Estudiante(grupo=grupo, numero_de_lista=numero_de_lista)
        estudiante.save()
        
        messages.success(request, 'El estudiante ha sido creado exitosamente')
        return redirect('chart')



def log(request):
    #Data
    latest_logs = list(Student.objects.order_by('date')[:5].values())

    #JsonResponse
    return JsonResponse(latest_logs, safe=False)

@csrf_protect
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else: 
            messages.error(request, "Usuario o contraseña incorrecta")
            return redirect("login")
    return render(request, "frontend/login.html")


def logout_user(request):
    logout(request)
    messages.success(request,("Logged out"))
    return redirect('login')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Usuario creado exitosamente")
                return redirect("index")
            else:
                messages.error(request, "Error al crear usuario")
                return redirect("register")
        else:
            messages.error(request, "Error al crear usuario")
            return redirect("register")
    else:
        form = RegisterUserForm()
        return render(request, "frontend/register_user.html", {"form": form})


class GuardarProgresook(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    
    #no entiendo por que existe get en CrearUsuario pero sirve jaja
    def get(self, request):
        questions = Pregunta.objects.all()
        #data = [{'Crear usuario:':'----'},{'Grupo':'Grupo 3'},{'Número de lista':'17'},{'Password':'*********'}]
        data = [
            {
                'questions':list(questions.values())
            }
        ]
        return JsonResponse(data, safe=False)
        
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        try:
            list_number = data['list_number']
            grupo = data['group']        
            pregunta = data['question']
            respuesta = data['answer']
            respuesta_alumno = data['resp_alumno']
            dificultad = data['difficulty']
            nivel = data['level']
            tiempo_asignado = data['assignedTime']
            fecha = data['dateTime']
            
        except KeyError as e:
            # Handle missing keys error
            error_message = [{"error": "Missing key: {}".format(e)}]
            return JsonResponse(error_message, safe=False)

        # Check if student already exists
        # me parece que no registra de nuevo pero no avisa correctamente
        pregunta_existente = Pregunta.objects.filter(list_number=list_number, grupo=grupo, pregunta=pregunta, respuesta=respuesta, respuesta_alumno = respuesta_alumno, dificultad=dificultad, nivel=nivel, tiempo_asignado=tiempo_asignado,  fecha=fecha).first()
        if pregunta_existente:
            error_message = [{"error": "La pregunta ya existe"}]
            return JsonResponse(error_message, safe=False)
        else:
            questionReg = Pregunta()
            questionReg.list_number = list_number
            questionReg.grupo = grupo 
            questionReg.pregunta = pregunta
            questionReg.respuesta = respuesta
            questionReg.respuesta_alumno = respuesta_alumno
            questionReg.dificultad = dificultad
            questionReg.nivel = nivel
            questionReg.tiempo_asignado = tiempo_asignado
            questionReg.fecha = fecha

            questionReg.save()
            success_message = [{"success": "Pregunta Guardada"}]
            return JsonResponse(success_message, safe=False)

class InicioSesion(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self, request):
        players = Pregunta.objects.all()
        data = [
            {
                'Player':list(players.values())
            }
        ]
        return JsonResponse(data, safe=False)

    def post(self,request):
        data = json.loads(request.body)
        data = json.loads(request.body.decode('utf-8'))
        try:
            list_number = data['list_number']
            grupo = data['group']
        except KeyError as e:
            error_message = [{"error": "Missing key: {}".format(e)}]
            return JsonResponse(error_message, safe=False)

        estudiante_existente = Estudiante.objects.filter(numero_de_lista=list_number, grupo=grupo).first()
        if estudiante_existente:
            last_level = Pregunta.objects.filter(list_number=list_number, grupo=grupo).latest('fecha').nivel
            difficulty = Pregunta.objects.filter(list_number=list_number, grupo=grupo).latest('fecha').dificultad
            success = [{'list_number': list_number, 'group': grupo, 'level': last_level, 'difficulty': difficulty}]
            return JsonResponse(success, safe=False)
        else:
            error_message = [{'list_number': '0', 'grupo': '0'}]
            return JsonResponse(error_message, safe=False)
