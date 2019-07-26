from django.contrib import admin

from courses.models import Course

from courses.forms import CourseAdminForm


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ('name', 'date_start', 'expiration_date', 'students', 'dropped_out_students', 'teachers')
    filter_horizontal = ('students', 'dropped_out_students', 'teachers')
    form = CourseAdminForm
    search_fields = ['__str__']

    class Media:
        js = (
            'admin/js/SelectBox.js',
            'admin/js/SelectFilter2.js',
            'admin/js/dropped_out_students_dynamic.js', )
