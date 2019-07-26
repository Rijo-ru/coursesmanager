from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db import models

from lectures.models import Lecture, AttendanceLecture
from lectures.forms import LectureAdminForm


class AttendanceLectureInline(admin.StackedInline):
    model = AttendanceLecture
    fields = ('student_full_name', 'date')
    readonly_fields = ('student_full_name', 'date')

    def student_full_name(self, obj=None):
        if obj:
            return obj.student.full_name

    student_full_name.short_description = 'Студент'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    fields = ('course', 'name', 'description', ('date_start', 'duration'), 'register_students', 'dropped_out_students',
              'teachers', 'link_to_qr',)
    readonly_fields = ('link_to_qr', 'link_token')
    list_filter = ['course__name']
    filter_horizontal = ('register_students', 'dropped_out_students', 'teachers')
    list_display = ('course', 'name', 'date_start', 'duration', 'count_register_students', 'count_marked_students')
    autocomplete_fields = ['course']
    search_fields = ['name']
    form = LectureAdminForm
    inlines = [AttendanceLectureInline, ]

    def count_register_students(self, obj=None):
        """Количесто зарегистрированных на лекцию студентов"""
        if obj:
            return obj.register_students.count()
        return 0
    count_register_students.admin_order_field = 'register_students__count'
    count_register_students.short_description = 'Зарегистрированно на лекцию'

    def count_dropped_out_students(self, obj=None):
        """Количество не допущенных к лекции"""
        if obj:
            return obj.dropped_out_students.count()
        return 0
    count_dropped_out_students.admin_order_field = 'dropped_out_students__count'
    count_dropped_out_students.short_description = 'Не допущено к лекции'

    def count_marked_students(self, obj=None):
        """Количество присутствующих на лекции"""
        if obj:
            return obj.marked_students.count()
        return 0
    count_marked_students.admin_order_field = 'marked_students__count'
    count_marked_students.short_description = 'Кол-во присутствующих'

    def link_to_qr(self, obj=None):
        if obj.id:
            return mark_safe(f'<a href="{reverse("qr_page", args={obj.id})}" target="_blank">OR CODE</a>')
        else:
            return 'Ссылка появится после сохранения.'
    link_to_qr.short_description = 'Страница с QR кодом'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(models.Count('register_students'),
                         models.Count('dropped_out_students'),
                         models.Count('marked_students'))
        return qs

    class Media:
        js = (
            'admin/js/SelectBox.js',
            'admin/js/SelectFilter2.js',
            'admin/js/dropped_out_students_dynamic.js',
            'admin/js/lectures.js'
        )
