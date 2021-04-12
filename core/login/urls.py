"""
Software-ArtPort
Fecha: 08 de abril del 2021 hora: 05:45 am
Última modificación a código
"""


from django.urls import path,include
from core.login.views import *

app_name = 'login'

urlpatterns = [
    path('',login.as_view(), name='ingresar'),
    path('logout/',LogoutView.as_view(), name='salir'),
    path('reset/password/',resetear_contrasenia.as_view(), name='resetear_password'),
    
]
