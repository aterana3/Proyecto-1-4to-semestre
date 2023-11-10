from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import UserProfileForm, StudentForm, TeacherForm, FacultadForm, CarreraForm, SemestreForm, AsignaturaForm, NotasForm
from .models import UserProfile, Student, Teacher, Facultad, Carrera, Semestre, Asignatura, Notas
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from PIL import Image
from django.db.models import Q
from django.db.models import Q

def home(request):
    context = {'title':'Instituto Tecnologico Unemi'}
    return render(request, 'home.html',context)

def register(request):
    if request.method == 'GET':
        context = {'title': 'Registro de Usuario', 'form': UserCreationForm()}
        return render(request, 'register.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                user_profile = UserProfile.objects.create(user=user)
                login(request, user)
                return redirect('home')
            except IntegrityError:
                context = {'title': 'Registro de Usuario', 'form': UserCreationForm(request.POST), 'error': 'Usuario ya existe'}
                return render(request, 'register.html', context)
        context = {'title': 'Registro de Usuario', 'form': UserCreationForm(request.POST), 'error': 'Password no coinciden'}
        return render(request, 'register.html', context)

def iniciarSesion(request):
    if request.method == 'GET':
        context = {'title':'Iniciar Sesion','form':AuthenticationForm}
        return render(request, 'login.html',context)
    else:
        print(request.POST)
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            context = {'title':'Iniciar Sesion','form':AuthenticationForm,'error':'Usuario o password incorrecto'}
            return render(request, 'login.html',context) 
        else:
            login(request,user) # crea una cooki del usuario registrado - guardar session
            return redirect('home')

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'GET':
        context = {'title': 'Perfil de Usuario', 'form': UserProfileForm()}
        return render(request, 'profile.html', context)
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                #Es la imagen que se subio
                profile_image = request.FILES.get('profile_image')
                #verificacion extra del formulario
                if not profile_image:
                    return render(request, 'profile.html', {"form": form, "error": "Por favor, seleccione una imagen"})          
                
                max_width = 800
                max_height = 600
                max_size = 2 * 1024 * 1024
                
                if profile_image.size > max_size:
                    return render(request, 'profile.html', {"form": form, "error": "La imagen es demasiado grande. El tamaño máximo permitido es 2MB"})
        
                img = Image.open(profile_image)
                width, height = img.size
                
                if width > max_width or height > max_height:
                    return render(request, 'profile.html', {"form": form, "error": "Las dimensiones de la imagen son demasiado grandes. El ancho máximo permitido es 800px y la altura máxima permitida es 600px"})
                
                form.save()
                return redirect('profile')
            else:
                return render(request, 'profile.html', {"form": form, "error": "Error de datos invalidos."})
        except:
            return render(request, 'profile.html', {"form": form, "error": "Error al actualizar perfil de usuario."})

#Una peticion tipo get que va a mandar un json con la ruta de la imagen si es que existe, caso contrario va a mandar un json con un "error"
@login_required
def get_profile_img(request):
    #Request GET
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if user_profile and user_profile.profile_image:
        return JsonResponse({'img': user_profile.profile_image.url})
    else:
        return JsonResponse({'error': 'No tiene imagen'})

#cargar los modelos no basados en usuarios
@login_required
def model_list(request, model, title, template, fields):
    context, objects = None, None
    try:
        q = request.GET.get('q')
        filter_conditions = Q()
        if q:
            for field in fields:
                filter_conditions |= Q(**{f'{field}__icontains': q})
        objects = model.objects.filter(filter_conditions)
        
        paginator = Paginator(objects,2)
        pagina = request.GET.get('page', 1)
        paginated_objects = paginator.get_page(pagina)
        context = {
            'objects': paginated_objects,
            'title': f'Consulta de {title}',
            'paginator': paginator,
            'num_pages': paginator.num_pages,
        }
        return render(request, template, context)
    except Exception as e:
        return render(request, template, {'title': f'Consulta de {title}', 'error': f'Ha ocurrido un error en la consulta: {e}'})

# cargar los modelos basados en usuarios
@login_required
def model_user_list(request, model, title, template, fields):
    context, objects = None, None
    try:
        q = request.GET.get('q')
        if q:
            filter_conditions = Q()
            for field in fields:
                filter_conditions |= Q(**{f'{field}__icontains': q})

            objects = model.objects.filter(Q(user=request.user) & filter_conditions)
        else:
            objects = model.objects.filter(user=request.user)

        paginator = Paginator(objects,2)
        pagina = request.GET.get('page', 1)
        paginated_objects = paginator.get_page(pagina)
        context = {
            'objects': paginated_objects,
            'title': f'Consulta de {title}',
            'paginator': paginator,
            'num_pages': paginator.num_pages,
        }
        return render(request, template, context)
    except Exception as e:
        return render(request, template, {'title': f'Consulta de {title}', 'error': f'Ha ocurrido un error en la consulta: {e}'})

# crud the students
@login_required
def student(request):
    return model_user_list(request, Student, "Estudiantes", "students.html", ["lastname", "firstname"])

@login_required
def create_student(request):
    form=None
    if request.method == "GET":
        context = {'title':'Registro de Estudiante','form':StudentForm,'error':''}
        return render(request, 'create_student.html',context)
    else:
        try:
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.user = request.user
                student.save()
                return redirect('students')
            else:
                return render(request, 'create_student.html', {"form": form, "error": "Error de datos invalidos."}) 
        except:
            return render(request, 'create_student.html', {"form": form, "error": "Error al Crear Registro de Estudiante."})

@login_required
def detail_student(request,id):
    student=None
    try:
        student = Student.objects.get(user=request.user,pk=id)
        # select * from stident where user="admin" and id=2
        student.graduate=True
        student.dategraduate=datetime.now()
        student.save()
        return redirect('students')
    except:
        context = {'title':'Datos del Estudiante','student':student,'error':'Error al seleccionar  estudiante'}
        return render(request, 'detail_student.html',context)  

@login_required
def update_student(request,id):
    student = Student.objects.filter(user=request.user,pk=id).first()
    form=None
    print(student)
    if request.method == "GET":
       form = StudentForm(instance=student)
       context = {'title':'Editar Estudiante','form':form,'error':''}
       return render(request, 'create_student.html',context)
    else:
        try:
            form = StudentForm(request.POST,instance=student)
            if form.is_valid():
                form.save()
                return redirect('students')
            else:
                return render(request, 'create_student.html', {"form": form, "error": "Error de datos invalidos."})  
        except:
            return render(request, 'create_student.html', {"form": form, "error": "Error al actualizar registro de Estudiante."})

@login_required
def delete_student(request,id):
    student=None
    try:
        student = Student.objects.get(user=request.user,pk=id)
        if request.method == "GET":
            context = {'title':'Estudiante a Eliminar','student':student,'error':''}
            return render(request, 'delete_student.html',context)  
        else: 
            student.delete()
            return redirect('students')
    except:
        context = {'title':'Datos del Estudiante','student':student,'error':'Error al eliminar estudiante'}
        return render(request, 'delete_student.html',context)  

#profesor
@login_required
def teacher(request):
    return model_user_list(request, Teacher, "Profesor", "teachers.html", ["lastname", "firstname"])

@login_required
def create_teacher(request):
    form = None
    if request.method == "GET":
        context = {'title':'Registro de Profesor','form':TeacherForm,'error':''}
        return render(request, 'create_teacher.html',context)
    else:
        try:
            form = TeacherForm(request.POST)
            if form.is_valid():
                teacher = form.save(commit=False)
                teacher.user = request.user
                teacher.save()
                return redirect('teachers')
            else:
                return render(request, 'create_teacher.html', {"form": form, "error": "Error de datos invalidos."}) 
        except:
            return render(request, 'create_teacher.html', {"form": form, "error": "Error al Crear Registro de Profesor."})

@login_required
def update_teacher(request,id):
    teacher = Teacher.objects.filter(user=request.user,pk=id).first()
    form=None
    if request.method == "GET":
       form = TeacherForm(instance=teacher)
       context = {'title':'Editar Profesor','form':form,'error':''}
       return render(request, 'create_teacher.html',context)
    else:
        try:
            form = TeacherForm(request.POST,instance=student)
            if form.is_valid():
                form.save()
                return redirect('teachers')
            else:
                return render(request, 'create_teacher.html', {"form": form, "error": "Error de datos invalidos."})  
        except:
            return render(request, 'create_teacher.html', {"form": form, "error": "Error al actualizar registro de profesor."})

@login_required
def delete_teacher(request,id):
    teacher=None
    try:
        teacher = Teacher.objects.get(user=request.user,pk=id)
        if request.method == "GET":
            context = {'title':'Profesor a Eliminar','teacher':teacher,'error':''}
            return render(request, 'delete_teacher.html',context)  
        else: 
            teacher.delete()
            return redirect('teachers')
    except:
        context = {'title':'Datos del Profesor','teacher':teacher,'error':'Error al eliminar profesor'}
        return render(request, 'delete_teacher.html',context)
    
#faculta
@login_required
def facultad(request):
    return model_list(request, Facultad, "Facultad", "facultades.html", ["description"])

@login_required
def create_facultad(request):
    form = None
    if request.method == "GET":
        context = {'title':'Registro de Facultad','form':FacultadForm,'error':''}
        return render(request, 'create_facultad.html',context)
    else:
        try:
            form = FacultadForm(request.POST)
            if form.is_valid():
                facultad = form.save(commit=False)
                facultad.save()
                return redirect('facultades')
            else:
                return render(request, 'create_facultad.html', {"form": form, "error": "Error de datos invalidos."}) 
        except:
            return render(request, 'create_facultad.html', {"form": form, "error": "Error al Crear Registro de Facultad."})

@login_required
def update_facultad(request, id):
    facultad = Facultad.objects.get(id=id)
    form = None
    if request.method == "GET":
       form = FacultadForm(instance=facultad)
       context = {'title': 'Editar Facultad', 'form': form, 'error': ''}
       return render(request, 'create_facultad.html', context)
    else:
        try:
            form = FacultadForm(request.POST, instance=facultad)
            if form.is_valid():
                form.save()
                return redirect('facultades')
            else:
                return render(request, 'create_facultad.html', {"form": form, "error": "Error de datos inválidos."})
        except:
            return render(request, 'create_facultad.html', {"form": form, "error": "Error al actualizar registro de Facultad."})


@login_required
def delete_facultad(request, id):
    facultad = None
    try:
        facultad = Facultad.objects.get(id=id)
        if request.method == "GET":
            context = {'title': 'Facultad a Eliminar', 'facultad': facultad, 'error': ''}
            return render(request, 'delete_facultad.html', context)
        else:
            facultad.delete()
            return redirect('facultades')
    except:
        context = {'title': 'Datos del Facultad', 'facultad': facultad, 'error': 'Error al eliminar facultad'}
        return render(request, 'delete_facultad.html', context)

#carrera
@login_required
def carrera(request):
    return model_list(request, Carrera, "Carrera", "carreras.html", ["description"])

@login_required
def create_carrera(request):
    form = None
    if request.method == "GET":
        context = {'title':'Registro de Carrera','form':CarreraForm,'error':''}
        return render(request, 'create_carrera.html',context)
    else:
        try:
            form = CarreraForm(request.POST)
            if form.is_valid():
                carrera = form.save(commit=False)
                carrera.save()
                return redirect('carreras')
            else:
                return render(request, 'create_carrera.html', {"form": form, "error": "Error de datos invalidos."}) 
        except:
            return render(request, 'create_carrera.html', {"form": form, "error": "Error al Crear Registro de Carrera."})
        
@login_required
def update_carrera(request,id):
    carrera = Carrera.objects.get(id=id)
    form = None
    if request.method == "GET":
       form = CarreraForm(instance=carrera)
       context = {'title': 'Editar Carrera', 'form': form, 'error': ''}
       return render(request, 'create_carrera.html', context)
    else:
        try:
            form = CarreraForm(request.POST, instance=carrera)
            if form.is_valid():
                form.save()
                return redirect('carreras')
            else:
                return render(request, 'create_carrera.html', {"form": form, "error": "Error de datos inválidos."})
        except:
            return render(request, 'create_carrera.html', {"form": form, "error": "Error al actualizar registro de Carrera."})

@login_required
def delete_carrera(request,id):
    carrera=None
    try:
        carrera = Carrera.objects.get(id=id)
        if request.method == "GET":
            context = {'title':'Carrera a Eliminar','carrera':carrera,'error':''}
            return render(request, 'delete_carrera.html',context)  
        else: 
            carrera.delete()
            return redirect('carreras')
    except:
        context = {'title':'Datos del Carrera','carrera':carrera,'error':'Error al eliminar carrera'}
        return render(request, 'delete_carrera.html',context)
    
#semestre
@login_required
def semestre(request):
    return model_list(request, Semestre, "Semestre", "semestres.html", ["description"])

@login_required
def create_semestre(request):
    form = None
    if request.method == "GET":
        context = {'title':'Registro de Semestre','form':SemestreForm,'error':''}
        return render(request, 'create_semestre.html',context)
    else:
        try:
            form = SemestreForm(request.POST)
            if form.is_valid():
                semestre = form.save(commit=False)
                semestre.save()
                return redirect('semestres')
            else:
                return render(request, 'create_semestre.html', {"form": form, "error": "Error de datos invalidos."}) 
        except:
            return render(request, 'create_semestre.html', {"form": form, "error": "Error al Crear Registro de Semestre."})

@login_required
def update_semestre(request,id):
    semestre = Semestre.objects.get(id=id)
    form = None
    if request.method == "GET":
       form = SemestreForm(instance=semestre)
       context = {'title': 'Editar Semestre', 'form': form, 'error': ''}
       return render(request, 'create_semestre.html', context)
    else:
        try:
            form = SemestreForm(request.POST, instance=semestre)
            if form.is_valid():
                form.save()
                return redirect('semestres')
            else:
                return render(request, 'create_semestre.html', {"form": form, "error": "Error de datos inválidos."})
        except:
            return render(request, 'create_semestre.html', {"form": form, "error": "Error al actualizar registro de Semestre."})
   
@login_required
def delete_semestre(request,id):
    semestre=None
    try:
        semestre = Semestre.objects.get(id=id)
        if request.method == "GET":
            context = {'title':'Semestre a Eliminar','semestre':semestre,'error':''}
            return render(request, 'delete_semestre.html',context)  
        else: 
            semestre.delete()
            return redirect('semestres')
    except:
        context = {'title':'Datos del Semestre','semestre':semestre,'error':'Error al eliminar semestre'}
        return render(request, 'delete_semestre.html',context)
        
#asignatura
@login_required
def asignatura(request):
    return model_list(request, Asignatura, "Asignatura", "asignaturas.html", ["description"])

@login_required
def create_asignatura(request):
    form = None
    if request.method == "GET":
        context = {'title':'Registro de Asignatura','form':AsignaturaForm,'error':''}
        return render(request, 'create_asignatura.html',context)
    else:
        try:
            form = AsignaturaForm(request.POST)
            if form.is_valid():
                asignatura = form.save(commit=False)
                asignatura.save()
                return redirect('asignaturas')
            else:
                return render(request, 'create_asignatura.html', {"form": form, "error": "Error de datos invalidos."}) 
        except:
            return render(request, 'create_asignatura.html', {"form": form, "error": "Error al Crear Registro de Asignatura."})
        
@login_required
def update_asignatura(request,id):
    asignatura = Asignatura.objects.get(id=id)
    form = None
    if request.method == "GET":
       form = AsignaturaForm(instance=asignatura)
       context = {'title': 'Editar Asignatura', 'form': form, 'error': ''}
       return render(request, 'create_asignatura.html', context)
    else:
        try:
            form = AsignaturaForm(request.POST, instance=asignatura)
            if form.is_valid():
                form.save()
                return redirect('asignaturas')
            else:
                return render(request, 'create_asignatura.html', {"form": form, "error": "Error de datos inválidos."})
        except:
            return render(request, 'create_asignatura.html', {"form": form, "error": "Error al actualizar registro de Asignatura."})
        
@login_required
def delete_asignatura(request,id):
    asignatura=None
    try:
        asignatura = Asignatura.objects.get(id=id)
        if request.method == "GET":
            context = {'title':'Asignatura a Eliminar','asignatura':asignatura,'error':''}
            return render(request, 'delete_asignatura.html',context)  
        else: 
            asignatura.delete()
            return redirect('asignaturas')
    except:
        context = {'title':'Datos del Asignatura','asignatura':asignatura,'error':'Error al eliminar asignatura'}
        return render(request, 'delete_asignatura.html',context)
    
#notas
@login_required
def notas(request):
    return model_list(request, Notas, "Notas", "notas.html", ["student__firstname", "student__lastname"])

@login_required
def create_nota(request):
    form = None
    if request.method == "GET":
        context = {'title':'Registro de Notas','form':NotasForm,'error':''}
        return render(request, 'create_nota.html',context)
    else:
        try:
            form = NotasForm(request.POST)
            if form.is_valid():
                notas = form.save(commit=False)
                notas.save()
                return redirect('notas')
            else:
                return render(request, 'create_nota.html', {"form": form, "error": "Error de datos invalidos."}) 
        except:
            return render(request, 'create_nota.html', {"form": form, "error": "Error al Crear Registro de Notas."})
        
@login_required
def update_nota(request,id):
    notas = Notas.objects.get(id=id)
    form = None
    if request.method == "GET":
       form = NotasForm(instance=notas)
       context = {'title': 'Editar Notas', 'form': form, 'error': ''}
       return render(request, 'create_nota.html', context)
    else:
        try:
            form = NotasForm(request.POST, instance=notas)
            if form.is_valid():
                form.save()
                return redirect('notas')
            else:
                return render(request, 'create_nota.html', {"form": form, "error": "Error de datos inválidos."})
        except:
            return render(request, 'create_nota.html', {"form": form, "error": "Error al actualizar registro de Notas."})
        
@login_required
def delete_nota(request,id):
    notas=None
    try:
        notas = Notas.objects.get(id=id)
        if request.method == "GET":
            context = {'title':'Notas a Eliminar','notas':notas,'error':''}
            return render(request, 'delete_nota.html',context)  
        else: 
            notas.delete()
            return redirect('notas')
    except:
        context = {'title':'Datos del Notas','notas':notas,'error':'Error al eliminar notas'}
        return render(request, 'delete_nota.html',context)