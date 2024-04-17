"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))
    
    
class AnketaForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    city = forms.CharField(label='Город', max_length=100)
    job = forms.CharField(label='Специальность', max_length=100)
    gender_choices = [
        ('1', 'Мужской'),
        ('2', 'Женский'),
    ]
    gender = forms.ChoiceField(label='Пол', choices=gender_choices, initial='male', widget=forms.RadioSelect)
    internet_choices = [
        ('1', 'Редко'),
        ('2', 'Иногда'),
        ('3', 'Часто'),
    ]
    internet = forms.ChoiceField(label='Частота использования интернета', choices=internet_choices, initial='often')
    email = forms.EmailField(label='E-mail', max_length=100)
    notice = forms.BooleanField(label='Получать новости сайта', required=False)
    message = forms.CharField(label='Короткое резюме', widget=forms.Textarea)
