from django.db import models


from students.models import Student
from teachers.models import Teacher


class Course(models.Model):
    name = models.CharField('Название курса', max_length=255)
    date_start = models.DateField('Дата начала курсов')
    expiration_date = models.DateField('Дата окончания курсов')

    students = models.ManyToManyField(
        Student,
        related_name='courses',
        verbose_name='Студенты',
        blank=True
    )

    teachers = models.ManyToManyField(
        Teacher,
        related_name='courses',
        verbose_name='Преподаватели',
        blank=True
    )

    dropped_out_students = models.ManyToManyField(
        Student,
        related_name='dropped_out_from_course',
        verbose_name='Выбыли с курса',
        blank=True
    )

    def __str__(self):
        return f'Курс "{self.name}"'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
