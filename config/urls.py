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


urlpatterns = [
    # Para administración directamente en Django
    path('admin/', admin.site.urls),
    
    # Para página web informativa
    path('',IndexView.as_view(), name='pagina_web'),

    # Para login y logout
    path('login/',include('core.login.urls'), name='inicio_sesion'),

    path('', IndexView.as_view()),
]
