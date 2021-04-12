"""
Software-ArtPort
Fecha: 08 de abril del 2021 hora: 06:08 am
Última modificación a código
"""
from django.contrib import admin
from django.urls import path,include
from core.homepage.views import IndexView

# para pruebas borrar en producción
from config.test import *

# Importanto para login
from core.login.views import login

# Importanto para inicio usuario
from core.Usuario.urls import *



urlpatterns = [
    # Para administración directamente en Django
    path('admin/', admin.site.urls),
    
    # Para página web informativa
    path('',IndexView.as_view(), name='pagina_web'),

    # Para login y logout
    path('login/',include('core.login.urls'), name='inicio_sesion'),

    # Para pantalla inicial luego de iniciar sesión de Usuario
    path('perfil/',include('core.Usuario.urls'), name='perfil_inicio'),

    path('prueba/', vista_prueba.as_view()),
]
