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

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)