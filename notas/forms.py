from django.forms import ModelForm, ImageField, FileInput
from .models import UserProfile, Student, Teacher, Facultad, Carrera, Semestre, Asignatura, Notas
#Los formularios se utilizan para la creacion de los objetos por medio de campos que se van a visualizar en la pagina
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
    profile_image = ImageField(widget=FileInput(attrs={'class': 'form-control-file'}))

    
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'graduate']
        
class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['firstname', 'lastname', 'user']

class FacultadForm(ModelForm):
    class Meta:
        model = Facultad
        fields = ['description', 'isactive']

class CarreraForm(ModelForm):
    class Meta:
        model = Carrera
        fields = ['facultad', 'description', 'isactive']

class SemestreForm(ModelForm):
    class Meta:
        model = Semestre
        fields = ['description', 'isactive']

class AsignaturaForm(ModelForm):
    class Meta:
        model = Asignatura
        fields = ['description', 'isactive']

class NotasForm(ModelForm):
    class Meta:
        model = Notas
        fields = ['student', 'asignatura', 'teacher', 'semestre', 'carrera', 'facultad', 'n1', 'n2', 'ex1', 'n3', 'n4', 'ex2', 'isaproved', 'isactive']