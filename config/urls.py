"""
Software-ArtPort
Fecha: 08 de abril del 2021 hora: 06:08 am
Última modificación a código
"""
from django.contrib import admin
from django.urls import path,include,re_path
from core.homepage.views import IndexView

# para pruebas borrar en producción
from config.test import *

# Importanto para login
from core.login.views import *

# Importanto para inicio usuario
from core.Usuario.urls.usuario.urls import *
from core.Usuario.urls.perfiles_roles.urls import *
from core.Usuario.urls.permisos.urls import *
from core.Usuario.urls.politicas_contrasenia.urls import *

# Para imagenes 
from django.conf import settings
from django.conf.urls.static import static 


#r '' especifica que la cadena es una cadena sin formato. '^' significa el comienzo y $ marca el final. 
#El caracter acento circunflejo (^) y el carácter signo de dólar ($) son importantes. El acento circunflejo significa que 
# #"requiere que el patrón concuerde con el inicio de la cadena de caracteres", y el signo de dólar significa que "exige que el patrón concuerde con el fin de la cadena"


urlpatterns = [
    # Para administración directamente en Django
    path('admin/', admin.site.urls),
    
    # Para página web informativa
    path('',IndexView.as_view(), name='pagina_web'),

    # Para login y logout
    path('login/',include('core.login.urls'), name='inicio_sesion'),

    # Para pantalla inicial luego de iniciar sesión de Usuario
    path('usuario/',include('core.Usuario.urls.usuario.urls'), name='perfil_inicio'),

    # Para perfiles de Usuario
    path('perfilesUsuario/',include('core.Usuario.urls.perfiles_roles.urls'), name='perfiles_de_usuarios'),

    # Para asignar permisos de Usuario
    path('permisos/',include('core.Usuario.urls.permisos.urls'), name='permisos'),

    # Para asignar política de contraseña de Usuario
    path('politicaContrasenia/',include('core.Usuario.urls.politicas_contrasenia.urls'), name='politicas_contrasenia'),

    # Link para pruebas borrar en producción 
    path('prueba/', vista_prueba.as_view()),

    
]
# Agregamos esta línea para archivos MEDIA
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
