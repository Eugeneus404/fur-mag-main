"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('partners/', views.partners, name='partners'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('anketa/', views.anketa, name='anketa'),
    path('registration/', views.registration, name='registration'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:item1>/<str:item2>/<str:item3>/', views.dynamic3, name='dynamic3'),
    path('catalog/<str:item1>/<str:item2>/', views.dynamic2, name='dynamic2'),
    path('catalog/<str:item1>/', views.dynamic1, name='dynamic1'),
]

handler404 = views.error_404