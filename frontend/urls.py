from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('index', views.index, name="index"),
    path('aboutus', views.aboutus, name="aboutus"),
    path('chart',views.chart,name="chart"),
    path('log',views.log, name="log"),
    path('login',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('register',views.register_user,name='register'),
    path('student_results/', views.student_results, name='student_results'),
    path('results/<int:list_number>/<str:grupo>/', views.student_results2, name='student_results2'),
    path('iniciosesion', views.InicioSesion.as_view()),
    path('guardarprogresook', views.GuardarProgresook.as_view()),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('crear-estudiante/', views.crear_estudiante, name='crear_estudiante')
]
