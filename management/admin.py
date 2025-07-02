from django.contrib import admin
from .models import Student, Subject, StudentSubject

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(StudentSubject)