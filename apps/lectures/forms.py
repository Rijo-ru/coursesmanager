from django import forms
from django.db.models import Q

from students.models import Student
from teachers.models import Teacher


class LectureAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """Смотрим что студент зачислен на курс и не выбыл с курса или уже был отмечен на лекции"""
        super().__init__(*args, **kwargs)
        if self.initial:
            self.fields['register_students'].queryset = Student.objects.filter(
                Q(courses__in=[self.instance.course]),
                ~Q(dropped_out_from_course__in=[self.instance.course])
                | Q(attended_lectures__lecture__in=[self.instance])
            )
            self.fields['dropped_out_students'].queryset = Student.objects.filter(
                Q(lectures__in=[self.instance])
            )
            self.fields['teachers'].queryset = Teacher.objects.filter(
                Q(courses__in=[self.instance.course])
            )
        else:
            self.fields['register_students'].queryset = Student.objects.none()
            self.fields['dropped_out_students'].queryset = Student.objects.none()
            self.fields['teachers'].queryset = Teacher.objects.none()

        self.fields['dropped_out_students'].widget.can_add_related = False
        self.fields['register_students'].widget.can_add_related = False
        self.fields['course'].widget.can_add_related = False
        self.fields['course'].widget.can_change_related = False

    def clean_course(self):
        cleaned_data = self.cleaned_data['course']
        if not self.initial:
            self.fields['register_students'].queryset = Student.objects.filter(
                Q(courses__in=[cleaned_data]),
                ~Q(dropped_out_from_course__in=[cleaned_data]))
        else:
            self.fields['register_students'].queryset = Student.objects.filter(
                Q(courses__in=[cleaned_data]),
                ~Q(dropped_out_from_course__in=[cleaned_data]) | Q(
                    attended_lectures__lecture__in=[self.instance])
            )
        self.fields['teachers'].queryset = Teacher.objects.filter(
            Q(courses__in=[cleaned_data])
        )
        return cleaned_data

    def clean_register_students(self):
        cleaned_data = self.cleaned_data['register_students']
        self.fields['dropped_out_students'].queryset = Student.objects.filter(
            Q(lectures__in=[self.instance]) | Q(pk__in=cleaned_data)
        )
        return cleaned_data

    def clean_date_start(self):
        data = self.cleaned_data['date_start']
        course_date_start = self.cleaned_data['course'].date_start
        if course_date_start > data.date():
            raise forms.ValidationError(
                f'Дата лекции, должна быть не раньше начала курса '
                f'({course_date_start.strftime("%d.%m.%Y")}).'
            )
        return data
