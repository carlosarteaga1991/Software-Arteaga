"""
Software-ArtPort
Fecha: 08 de abril del 2021 hora: 05:45 am
Última modificación a código
"""

from django import forms
from django.contrib.admin import widgets

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from core.Usuario.models import *
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.urls import reverse_lazy

from core.Usuario.models import *


class form_reseteo_contrasenia(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Ingrese su Usuario',
            'class': 'form-control',
            'autocomplete': 'false'
        }
    ))

    # sobre escribimos el método clean para validar si el usuario existe
    def clean(self):
        cleaned = super().clean()
        if not usuario.objects.filter(username=cleaned['username']).exists():
            #para  mostrar los errores para quitarle '_all_'
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('El usuario no existe')
            #raise forms.ValidationError('El usuario no existe')
        return cleaned

    # El siguiente método es para obtener el usuario
    def get_user(self):
        username = self.cleaned_data.get('username')
        return usuario.objects.get(username=username)

class form_link_reseteo_contrasenia(forms.Form):
    polit_contrasenia = politicas_contrasenia.objects.get()
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Ingrese su nueva contraseña',
            'class': 'form-control',
            'autocomplete': 'false',
            'id': 'pass',
            'minlength': polit_contrasenia.longitud_minima_contrasenia,
            'maxlength': polit_contrasenia.longitud_maxima_contrasenia,
            #'onkeyup': 'caracteresContrasenia(value)'
        }
    ))

    confirmar_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirme su contraseña',
            'class': 'form-control',
            'autocomplete': 'false',
            'id': 'pass2',
            'onkeyup': 'validarContrasenia(value)',
            'minlength': polit_contrasenia.longitud_minima_contrasenia,
            'maxlength': polit_contrasenia.longitud_maxima_contrasenia,
        }
    ))

    # sobre escribimos el método clean para validar si el usuario existe
    def clean(self):
        cleaned = super().clean()
        # Optenemos las contraseñas ingresadas por el usuario
        password = cleaned['password']
        confirmar_password = cleaned['confirmar_password']

        if password != confirmar_password:
            #para  mostrar los errores para quitarle '_all_'
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('Las contraseñas no son iguales')
            #raise forms.ValidationError('El usuario no existe')
        return cleaned

    # El siguiente método es para obtener el usuario
    def get_user(self):
        username = self.cleaned_data.get('username')
        return usuario.objects.get(username=username)