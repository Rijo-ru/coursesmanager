from django.contrib import admin

from teachers.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    search_fields = ['surname', 'name',  'last_name']
    list_display = ('full_name', )
    list_filter = ['courses__name']

    def full_name(self, obj=None):
        if obj:
            return obj.full_name
        return ''
    full_name.short_description = 'ФИО'
