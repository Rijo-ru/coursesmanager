import random
import string

from django.db import models


class Student(models.Model):
    surname = models.CharField('Фамилия', max_length=255)
    name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Отчество', max_length=255, blank=True, null=True)

    phone_number = models.CharField('Номер телефона',
                                    help_text='Номер телефона, без кода страны. Например: 9123456789',
                                    max_length=20, unique=True)
    email = models.CharField('E-Mail', max_length=255, blank=True, null=False)

    identity_token = models.CharField('Токен пользователя', max_length=32, unique=True)

    full_name = models.CharField('ФИО', max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.identity_token:
            self.identity_token = self._random_token()
        if self.full_name != self.calc_full_name() or not self.full_name:
            self.full_name = self.calc_full_name()
        super().save(*args, **kwargs)

    def _random_token(self):
        length_string = self._meta.get_field('identity_token').max_length
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length_string))

    def calc_full_name(self):
        return f'{self.surname.capitalize()} {self.name.capitalize()} {(self.last_name or "").capitalize()}'

    @property
    def incognito_name(self):
        return f'{self.name.capitalize()} {(self.last_name or "").capitalize()} {self.surname.capitalize()[0]}.'

    def __str__(self):
        return self.calc_full_name()

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'



