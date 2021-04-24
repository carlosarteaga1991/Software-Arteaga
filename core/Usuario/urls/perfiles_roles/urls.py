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
from core.Usuario.views.perfiles_roles.views import *

app_name = 'perfiles_roles'

urlpatterns = [


    # Para listar perfiles (SÍ requiere permisos) 
    path('listar/',listar_roles.as_view(), name='listar_perfiles_roles'), 

    # Para crear perfiles (SÍ requiere permisos) 
    path('crear/',crear_roles.as_view(), name='crear_perfiles_roles'), 

    # Para editar perfiles (SÍ requiere permisos) 
    path('editar/<int:pk>/',editar_roles.as_view(), name='editar_perfiles_roles'), 

    # Para borrar perfiles (SÍ requiere permisos) 
    path('borrar/<int:pk>/',borrar_roles.as_view(), name='borrar_perfiles_roles'), 

]