"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from notas import views
from core import settings
from django.conf.urls.static import static

# urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('register/', views.register,name='register'),
    path('login/', views.iniciarSesion,name='login'),
    path('logout/', views.cerrarSesion,name='logout'),
    path('profile/', views.profile, name='profile'),
    path('get_profile_img/', views.get_profile_img, name='get_profile_img'),
    path('students/', views.student,name='students'),
    path('students/create/', views.create_student,name='create_student'),
    path('students/<int:id>/', views.detail_student,name='detail_student'),
    path('students/update/<int:id>/', views.update_student,name='update_student'),
    path('students/delete/<int:id>/', views.delete_student,name='delete_student'),
    path('teachers/', views.teacher,name="teachers"),
    path('teachers/create/', views.create_teacher, name='create_teacher'),
    path('teachers/update/<int:id>/', views.update_teacher,name='update_teacher'),
    path('teachers/delete/<int:id>/', views.delete_teacher,name='delete_teacher'),
    path('facultades/', views.facultad,name="facultades"),
    path('facultades/create/', views.create_facultad, name='create_facultad'),
    path('facultades/update/<int:id>/', views.update_facultad,name='update_facultad'),
    path('facultades/delete/<int:id>/', views.delete_facultad,name='delete_facultad'),
    path('carreras/', views.carrera,name="carreras"),
    path('carreras/create/', views.create_carrera, name='create_carrera'),
    path('carreras/update/<int:id>/', views.update_carrera,name='update_carrera'),
    path('carreras/delete/<int:id>/', views.delete_carrera,name='delete_carrera'),
    path('semestres/', views.semestre,name="semestres"),
    path('semestres/create/', views.create_semestre, name='create_semestre'),
    path('semestres/update/<int:id>/', views.update_semestre,name='update_semestre'),
    path('semestres/delete/<int:id>/', views.delete_semestre,name='delete_semestre'),
    path('asignaturas/', views.asignatura,name="asignaturas"),
    path('asignaturas/create/', views.create_asignatura, name='create_asignatura'),
    path('asignaturas/update/<int:id>/', views.update_asignatura,name='update_asignatura'),
    path('asignaturas/delete/<int:id>/', views.delete_asignatura,name='delete_asignatura'),
    path('notas/', views.notas,name="notas"),
    path('notas/create/', views.create_nota, name='create_nota'),
    path('notas/update/<int:id>/', views.update_nota,name='update_nota'),
    path('notas/delete/<int:id>/', views.delete_nota,name='delete_nota'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)