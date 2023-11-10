from django.db import models
from django.contrib.auth.models import User

#son los distintos objetos con sus respectivos "atributos" que manejara la base de datos y el proyecto en general
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField('Imagen de Perfil', upload_to='profile_images/', null=True, blank=True)

    class Meta:
        verbose_name = ('Perfil de Usuario')
        verbose_name_plural = ('Perfiles de Usuarios')

    def __str__(self):
        return self.user.username

class Student(models.Model):
    firstname = models.CharField('Nombres', max_length=200)
    lastname = models.CharField(verbose_name="Apellidos", max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    dategraduate = models.DateTimeField('Fecha Graduacion', null=True, blank=True)
    graduate = models.BooleanField('Graduado', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('Estudiante')
        verbose_name_plural = ('Estudiantes')
        ordering = ['-lastname']

    def __str__(self):
        return f"{self.lastname} {self.firstname} -  {self.user.username}"
    
class Teacher(models.Model):
    firstname = models.CharField('Nombres', max_length=200)
    lastname = models.CharField(verbose_name="Apellidos", max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ('Teacher')
        verbose_name_plural = ('Teacheres')
        ordering = ['-lastname']

    def __str__(self):
        return f"{self.lastname} {self.firstname} -  {self.user.username}"

class Facultad(models.Model):
    description = models.CharField('Descripcion', max_length=200)
    isactive = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = ('Facultad')
        verbose_name_plural = ('Facultades')
        ordering = ['description']

    def __str__(self):
        return f"{self.description}"

class Carrera(models.Model):
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    description = models.CharField('Descripcion', max_length=200)
    isactive = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = ('Carrera')
        verbose_name_plural = ('Carreras')
        ordering = ['description']

    def __str__(self):
        return f"{self.description} - {self.facultad}"

class Semestre(models.Model):
    description = models.CharField('Descripcion', max_length=200)
    isactive = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = ('Semestre')
        verbose_name_plural = ('Semestres')
        ordering = ['description']

    def __str__(self):
        return f"{self.description}"

class Asignatura(models.Model):
    description = models.CharField('Descripcion', max_length=200)
    isactive = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = ('Asignatura')
        verbose_name_plural = ('Asignaturas')
        ordering = ['description']

    def __str__(self):
        return f"{self.description}"
    
class Notas(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    n1 = models.IntegerField('n1')
    n2 = models.IntegerField('n2')
    ex1 = models.IntegerField('ex1')
    n3 = models.IntegerField('n3')
    n4 = models.IntegerField('n4')
    ex2 = models.IntegerField('ex2')
    isaproved = models.BooleanField('Aprobado', default=False)
    isactive = models.BooleanField('Estado', default=True)
    created = models.DateTimeField('Fecha de Creación', auto_now_add=True)

    class Meta:
        verbose_name = ('Nota')
        verbose_name_plural = ('Notas')
        ordering = ['student', 'asignatura']