"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import AnketaForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )


def anketa(request):
    assert isinstance(request, HttpRequest)
    
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {'1': 'Каждый день', '2': 'Несколько раз в день', '3': 'Несколько раз в неделю', '4': 'Несколько раз в месяц'}

    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'city': form.cleaned_data['city'],
                'job': form.cleaned_data['job'],
                'gender': gender.get(form.cleaned_data['gender'], ''),
                'internet': internet.get(form.cleaned_data['internet'], ''),
                'notice': 'Да' if form.cleaned_data['notice'] else 'Нет',
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
        else:
            data = None
    else:
        form = AnketaForm()
        data = None
    
    return render(request, 'app/anketa.html', {'form': form, 'data': data})

def registration(request):
    """Renders the registration page."""
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            regform.last_login = datetime.now()
            
            regform.save()
            
            return redirect("home")
    else:
        regform = UserCreationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/registration.html",
        {
            'regform': regform,
            'year': datetime.now().year,
            'title':'Регистрация',
        }
    )
