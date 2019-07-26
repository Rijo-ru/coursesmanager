from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe


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
    fields = ('course', 'name', 'description', 'date_start', 'register_students', 'dropped_out_students',
              'teachers', 'link_to_qr', 'link_token')
    readonly_fields = ('link_to_qr', 'link_token')
    list_filter = ['course__name']
    filter_horizontal = ('register_students', 'dropped_out_students', 'teachers')
    autocomplete_fields = ['course']
    form = LectureAdminForm
    inlines = [AttendanceLectureInline, ]

    def link_to_qr(self, obj=None):
        if obj.id:
            return mark_safe(f'<a href="{reverse("qr_page", args={obj.id})}" target="_blank">OR CODE</a>')
        else:
            return 'Ссылка появится после сохранения.'

    link_to_qr.short_description = 'Страница с QR кодом'

    class Media:
        js = (
            'admin/js/SelectBox.js',
            'admin/js/SelectFilter2.js',
            'admin/js/dropped_out_students_dynamic.js',
            'admin/js/lectures.js'
        )
