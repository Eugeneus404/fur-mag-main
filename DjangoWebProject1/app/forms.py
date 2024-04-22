"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.files.images import get_image_dimensions
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        labels = {'avatar': ''}
        
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
        
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control custom-input',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control custom-input',
                                   'placeholder':'Пароль'}))
    
class BootstrapUserCreationForm(UserCreationForm):
    """User creation form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control custom-input',
                                   'placeholder': 'Имя пользователя'}))
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput({
                                    'class': 'form-control custom-input',
                                    'placeholder': 'Пароль'}))
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput({
                                    'class': 'form-control custom-input',
                                    'placeholder': 'Подтверждение пароля'}))

class BootstrapPasswordChangeForm(PasswordChangeForm):
    """Password change form which uses bootstrap CSS."""
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput({
                                       'class': 'form-control custom-input',
                                       'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput({
                                        'class': 'form-control custom-input',
                                        'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput({
                                        'class': 'form-control custom-input',
                                        'placeholder': 'Подтверждение нового пароля'}))
    
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
