from django import forms
from django.db.models import Q

from students.models import Student


class CourseAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """Убираем возможность добавлять студента в список 'Выбыли с курса, предварительно не зачисленных на курс'"""
        super().__init__(*args, **kwargs)
        self.fields['dropped_out_students'].queryset = Student.objects.filter(
            courses__in=[self.instance]
        )
        self.fields['dropped_out_students'].widget.can_add_related = False

    def clean_students(self):
        """Обновляем список студентов, которые могут выбыть с курса"""
        cleaned_data = self.cleaned_data['students']
        self.fields['dropped_out_students'].queryset = Student.objects.filter(
            Q(courses__in=[self.instance]) | Q(pk__in=cleaned_data)
        )
        return cleaned_data
