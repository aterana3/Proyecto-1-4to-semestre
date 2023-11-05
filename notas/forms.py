from django.forms import ModelForm, ImageField, FileInput
from .models import Student, Facultad, UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
    profile_image = ImageField(widget=FileInput(attrs={'class': 'form-control-file'}))

    
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'graduate']
        
class FacultadForm(ModelForm):
    class Meta:
        model = Facultad
        fields = ['description', 'isactive']