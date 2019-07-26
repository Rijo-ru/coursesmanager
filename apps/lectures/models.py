import random
import string

from django.db import models
from django.utils import timezone

from courses.models import Course
from students.models import Student
from teachers.models import Teacher


class Lecture(models.Model):
    course = models.ForeignKey(Course,
                               related_name='lectures',
                               verbose_name='Курс',
                               on_delete=models.CASCADE)

    name = models.CharField('Наименование лекции', max_length=255)
    description = models.TextField('Описание', blank=True, null=True)

    date_start = models.DateTimeField('Дата/Время начала')
    duration = models.TimeField('Продолжительность лекции')

    teachers = models.ManyToManyField(
        Teacher,
        related_name='lectures',
        verbose_name='Преподаватель',
        blank=True
    )

    register_students = models.ManyToManyField(
        Student,
        related_name='lectures',
        verbose_name='Зарегистрированные на лекцию',
        blank=True
    )

    dropped_out_students = models.ManyToManyField(
        Student,
        related_name='dropped_out_from_lectures',
        verbose_name='Заблокирован доступ для',
        blank=True
    )

    link_token = models.CharField('Токен лекции', max_length=32, unique=True)

    def save(self, *args, **kwargs):
        if not self.link_token:
            self.link_token = self._random_token()
        super().save(*args, **kwargs)

    def _random_token(self):
        length_string = self._meta.get_field('link_token').max_length
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length_string))

    def __str__(self):
        return f'Лекция "{self.name}" начало в {timezone.localtime(self.date_start).strftime("%H:%M %d.%m.%Y")}'

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class AttendanceLecture(models.Model):
    """Модель записи отметки студента на лекцию"""
    lecture = models.ForeignKey(
        Lecture,
        related_name='marked_students',
        verbose_name='Лекция',
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        Student,
        related_name='attended_lectures',
        verbose_name='Студент',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        'Дата/Время',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self. student.full_name}  отметился на лекции {self.lecture.name} в {timezone.localtime(self.date).strftime("%H:%M %d.%m.%Y")}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lecture', 'student'], name='unique_attendance_lecture'),
        ]
        verbose_name = 'Отмеченный студент на лекции'
        verbose_name_plural = 'Отмеченные студенты на лекции'
