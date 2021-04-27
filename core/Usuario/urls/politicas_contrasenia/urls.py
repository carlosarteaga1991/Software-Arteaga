"""
Software-ArtPort
Fecha: 08 de abril del 2021 hora: 06:08 am
Última modificación a código
"""
from django.contrib import admin
from django.urls import path,include
from core.homepage.views import IndexView

# Importanto para login
from core.login.views import login

# Importanto para inicio usuario
from core.Usuario.views.usuario.views import *
from core.Usuario.views.politicas_contrasenia.views import *


#r '' especifica que la cadena es una cadena sin formato. '^' significa el comienzo y $ marca el final. 
#El caracter acento circunflejo (^) y el carácter signo de dólar ($) son importantes. El acento circunflejo significa que 
# #"requiere que el patrón concuerde con el inicio de la cadena de caracteres", y el signo de dólar significa que "exige que el patrón concuerde con el fin de la cadena"

app_name = 'politicas_contrasenia'

urlpatterns = [


    # Para listar perfiles (SÍ requiere permisos) 
    path('listar/',listar_politicas_contrasenia.as_view(), name='listar_politicas_contrasenia'), 

    # Para editar perfiles (SÍ requiere permisos) 
    #path(r'^editar/(?P<int:pk>\d+)/$',editar_politicas_contrasenia.as_view(), name='editar_politicas_contrasenia'), 
    path('editar/<int:pk>/',editar_politicas_contrasenia.as_view(), name='editar_politicas_contrasenia'),

 
]