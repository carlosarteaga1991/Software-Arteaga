"""
Software-ArtPort
Fecha: 06 de abril del 2021 hora: 20:13 pm
Última modificación a código
"""

from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


# Llave debe estar en variable global a pasar a producción
SECRET_KEY = os.getenv('SECRET_KEY_FIRST')






#'3^7-&j!1!9jc#-4r^5sm5b%!gy997@hhvgzm35+$#i_2spxh_^'

# Al pasar a producción debe estar en false
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Aplicaciones del Software

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Librerías
    'widget_tweaks',

    # Aplicaciones
    'core.homepage',
    'core.RRHH',
    'core.Usuario',
    'core.login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #se coloca os.path.join(BASE_DIR, 'templates') para q busq la carpeta templates
        'APP_DIRS': True, # esto si deseamos que busque en los templates de nuestras aplicaciones
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'




# Base de Datos

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db-softartpor',
        'USER': 'root',
        'PASSWORD': 'Art3aga_1',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Esto es para sustituir el nuevo modelo personalizado
AUTH_USER_MODEL = 'Usuario.usuario'

# Internationalization

LANGUAGE_CODE = 'es-hn'

TIME_ZONE = 'America/Tegucigalpa'

USE_I18N = True

USE_L10N = False # se colocó en False para que use bien la separación ejem. 1,524,000.25

USE_TZ = False


# Archivos estáticos (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# En producción colocar para enviar los estáticos:
#STATIC_ROOT = 'staticfiles'

# declaración de variable para usar archivos estáticos

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"), # _global
]


# para el login hay q indicarle a que URL nos dirigirá si es exitoso
#LOGIN_REDIRECT_URL = '/cobros/dashboard/'

# para q direcciones en caso de darle salir sesión
LOGOUT_REDIRECT_URL = '/login/'

# en caso de querer ingresar a una URL ya existente y no está loggeado un usuario que me direccione a:
LOGIN_URL = '/login/'

# Para alojar nuestros archivos media usamos:
#MEDIA_URL = '/media/'

# En producción colocar para enviar los estáticos:
#MEDIA_URL = '/'

#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#creamos la URL absoluta para acceder
