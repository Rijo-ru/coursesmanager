from django.contrib import admin

from students.models import Student
from students.forms import StudentAdminForm

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_filter = ['courses__name']
    exclude = ('identity_token', 'full_name')
    form = StudentAdminForm
