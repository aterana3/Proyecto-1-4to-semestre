from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
  firstname = models.CharField('Nombres',max_length=200)
  lastname = models.CharField(verbose_name="Apellidos",max_length=200)
  created = models.DateTimeField(auto_now_add=True)
  dategraduate = models.DateTimeField('Fecha Graduacion',null=True, blank=True)
  graduate = models.BooleanField('Graduado',default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  class Meta:
      verbose_name = ('Estudiante')
      verbose_name_plural = ('Estudiantes')
      ordering = ('-lastname',)

  def __str__(self):
    return f"{self.lastname} {self.firstname} -  {self.user.username}"
  
class Facultad(models.Model):
    description = models.CharField('Descripcion',max_length=200)
    isactive = models.BooleanField('Estado',default=True)
    
    class Meta:
      verbose_name = ('Facultad')
      verbose_name_plural = ('Facultades')
      ordering = ('description',)
      
    def __str__(self):
      return f"{self.description}"
  
class Carrera(models.Model):
    facultad = models.ForeignKey(Facultad,on_delete=models.CASCADE)
    description = models.CharField('Descripcion',max_length=200)
    isactive = models.BooleanField('Estado',default=True)
    
    class Meta:
      verbose_name = ('Carrera')
      verbose_name_plural = ('Carreras')
      ordering = ('description',)
      
    def __str__(self):
      return f"{self.description}"
    
# class Asignatura:
#   pass
# class profesor:
#   pass
# class Semestre:
#   pass
# class Notas:
#   pass
#   # guardar user: user = models.ForeignKey(User, on_delete=models.CASCADE)
  