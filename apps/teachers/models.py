from django.db import models


class Teacher(models.Model):
    surname = models.CharField('Фамилия', max_length=255)
    name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Отчество', max_length=255, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.surname.capitalize()} {self.name.capitalize()} {(self.last_name or "").capitalize()}'

    def __str__(self):
        return f'Преподаватель "{self.surname.capitalize()} {self.name.capitalize()} {(self.last_name or "").capitalize()}"'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
