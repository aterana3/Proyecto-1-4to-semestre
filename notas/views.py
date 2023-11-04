from datetime import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import StudentForm
from .models import Student
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# the homepage
def home(request):
    # return HttpResponse('<h1>Pagina de Inicio</h1>')
    #return JsonResponse({'pagina':"Principal","autor":"Daniel"})
    context = {'title':'Instituto Tecnologico Unemi'}
    return render(request, 'home.html',context)

# the users
def register(request):
    print(request.method,request.path,request.user)
    if request.method == 'GET':
        print(request.GET)
        context = {'title':'Registro de Usuario','form': UserCreationForm()}
        return render(request, 'register.html',context)
    else:
        print(request.POST,request.POST['username'],request.POST.get('password1'))
        if request.POST['password1'] == request.POST['password2']:
           try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save() 
                login(request,user) # crea una cooki del usuario registrado
                return redirect('home')
           except IntegrityError:
                context = {'title':'Registro de Usuario','form': UserCreationForm(request.POST),'error':'Usuario ya existe'}
                return render(request, 'register.html',context)
        context = {'title':'Registro de Usuario','form': UserCreationForm(request.POST),'error':'Password no coinciden'}
        return render(request, 'register.html',context)
    

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

# crud the students
@login_required
def student(request):
    context,students=None,None
    try:
        q = request.GET.get('q') # ver
        if q:
            students = Student.objects.filter(user=request.user,lastname__icontains=q)
            #  select * from Student where user=1 and lastname like "%ver%"
        else:
            students = Student.objects.filter(user=request.user)    
            # #  select * from Student  where user=1
        # Crea un paginador con los estudiantes
        print(students)
        paginator = Paginator(students,2)
        pagina = request.GET.get('page', 1)   # Obtén el número de página actual
        # Obtén los libros de la página actual
        students_paginados = paginator.get_page(pagina)
        # Envía el paginador con los estudiantes y el número de páginas al contexto
        context = {
            'students': students_paginados,
            'title':'Consulta de Estudiantes',
            'paginator': paginator,
            'num_pages': paginator.num_pages,
        }
      
        return render(request, 'students.html',context)
    except:
        return render(request, 'students.html',{'title':'Consulta de Estudiantes','error':'Ha ocurrido un error en la consulta'})

@login_required
def create_student(request):
    form=None
    if request.method == "GET":
        context = {'title':'Registro de Estudiante','form':StudentForm,'error':''}
        return render(request, 'create_student.html',context)
    else:
        try:
            form = StudentForm(request.POST)
            print(form)
            print(request.POST)
            print(request.user)
            if form.is_valid():
                student = form.save(commit=False)# lo tiene en memoria
                student.user = request.user
                student.save() # lo guarda en la BD
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
       