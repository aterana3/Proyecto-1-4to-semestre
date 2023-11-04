from django.contrib import admin

# Register your models here.
from .models import Student

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )

#admin.site.register(Student)
admin.site.register(Student, TaskAdmin)