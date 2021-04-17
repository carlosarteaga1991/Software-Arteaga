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
from core.Usuario.views import *

app_name = 'usuario'

urlpatterns = [

    # Para inicio de login exitoso y HOME (No requiere permisos)
    path('usuario/',inicio_usuario.as_view(), name='inicio'),

    # Para Editar Perfil desde configuración (No requiere permisos)
    path('usuario/editarPerfil/',editar_perfil_usuario.as_view(), name='editar_perfil'),

    # Para Editar Perfil desde configuración (No requiere permisos)
    path('usuario/editarPassword/',cambiar_password_usuario.as_view(), name='editar_contrasenia'),

]