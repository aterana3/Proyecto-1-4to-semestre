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
    path('students/', views.student,name='students'),
    path('students/create/', views.create_student,name='create_student'),
    path('students/<int:id>/', views.detail_student,name='detail_student'),
    path('students/update/<int:id>/', views.update_student,name='update_student'),
    path('students/delete/<int:id>/', views.delete_student,name='delete_student'),
    path('register/', views.register,name='register'),
    path('login/', views.iniciarSesion,name='login'),
    path('logout/', views.cerrarSesion,name='logout'),
    path('profile/', views.profile, name='profile'),
    path('get_profile_img/', views.get_profile_img, name='get_profile_img'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
