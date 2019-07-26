import re
from django import forms


class StudentAdminForm(forms.ModelForm):

    def clean_phone_number(self):
        raw_data = self.cleaned_data['phone_number']
        cleaned_data = re.sub(r'\D', '', raw_data)
        if len(cleaned_data) == 10:
            return cleaned_data
        raise forms.ValidationError('Номер телефона должен быть без кода страны, и состоять из 10 цифр.')


