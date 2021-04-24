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

app_name = 'usuario'

urlpatterns = [

    # Para inicio de login exitoso y HOME (No requiere permisos)
    path('',inicio_usuario.as_view(), name='inicio'),

    # Para Editar Perfil desde configuración (No requiere permisos)
    path('editarPerfil/',editar_perfil_usuario.as_view(), name='editar_perfil'),

    # Para Editar Perfil desde configuración (No requiere permisos)
    path('editarPassword/',cambiar_password_usuario.as_view(), name='editar_contrasenia'),

    # Para Listar usuarios (SÍ requiere permisos)
    path('listar/',listar_usuarios.as_view(), name='listar_usuarios'), 

    # Para editar usuarios (SÍ requiere permisos)
    path('editar/<int:pk>/',editar_usuario.as_view(), name='editar_usuarios'), 

    # Para borrar usuarios (SÍ requiere permisos)
    path('borrar/<int:pk>/',borrar_usuario.as_view(), name='borrar_usuarios'),

    # Para crear usuarios (SÍ requiere permisos)
    path('crear/',crear_usuario.as_view(), name='crear_usuarios'), 

    # Para primer ingreso usuarios (no requiere permisos)
    path('primerIngreso/',primer_ingreso_usuario.as_view(), name='primer_ingreso_usuarios'), 


]