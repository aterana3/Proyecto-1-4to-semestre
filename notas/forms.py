from django.forms import ModelForm
from .models import Student,Facultad

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'graduate']
        
class FacultadForm(ModelForm):
    class Meta:
        model = Facultad
        fields = ['description', 'isactive']