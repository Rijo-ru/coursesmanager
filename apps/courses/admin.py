from django.contrib import admin
from django.db import models

from courses.models import Course

from courses.forms import CourseAdminForm


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ('name', 'date_start', 'expiration_date', 'students', 'dropped_out_students', 'teachers')
    filter_horizontal = ('students', 'dropped_out_students', 'teachers')
    list_display = ('name', 'date_start', 'expiration_date',
                    'len_course_in_day', 'count_students', 'count_dropped_out_students', 'count_teachers')
    form = CourseAdminForm
    search_fields = ['name']

    def count_students(self, obj=None):
        """Количество студентов на курсе"""
        if obj:
            return obj.students.count()
        return 0
    count_students.admin_order_field = 'students__count'
    count_students.short_description = "Количество студентов"

    def count_dropped_out_students(self, obj=None):
        """Количество студентов выбывших с курса"""
        if obj:
            return obj.dropped_out_students.count()
        return 0
    count_dropped_out_students.admin_order_field = 'dropped_out_students__count'
    count_dropped_out_students.short_description = "Количество студентов выбывших с курса"

    def count_teachers(self, obj=None):
        """Количество преподавателей на курсе"""
        if obj:
            return obj.teachers.count()
        return 0
    count_teachers.admin_order_field = 'teachers__count'
    count_teachers.short_description = "Количество преподавателей"

    def len_course_in_day(self, obj=None):
        """Продолжительность курса в днях"""
        if obj:
            return (obj.expiration_date-obj.date_start).days + 1
    len_course_in_day.admin_order_field = 'len_course_in_day'
    len_course_in_day.short_description = "Продолжительность курса (в днях)"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(models.Count('students'), models.Count('teachers'), models.Count('dropped_out_students'),
                         len_course_in_day=models.F('expiration_date')-models.F('date_start'))
        return qs

    class Media:
        js = (
            'admin/js/SelectBox.js',
            'admin/js/SelectFilter2.js',
            'admin/js/dropped_out_students_dynamic.js', )
