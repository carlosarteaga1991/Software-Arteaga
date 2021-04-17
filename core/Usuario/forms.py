from django.forms import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.urls import reverse_lazy
from django.contrib.admin import widgets

from core.Usuario.models import *


class form_perfil_usuario(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            #form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombres'].widget.attrs['autofocus'] = True

    class Meta():
        model = usuario
        fields = '__all__'
        exclude = ['fch_ingreso_labores','fch_ultimo_login','fch_ultimo_cambio_contrasenia','intentos_fallidos','username','fch_modificacion','primer_ingreso','fch_cambio_password','usuario_modificacion','cambiar_contrasenia','estado','bloqueado','is_active','usuario_creacion','borrado','id_rol','password','last_login','ip_ultimo_acceso','usuario_administrador','id_departamento','id_puesto']

        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los primeros nombres',
                    'onkeypress': 'return nombre(event)',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'onkeypress': 'return nombre(event)',
                }
            ),
            'email': TextInput(
                attrs={
                    #'id': 'verificar',
                }
            )
    
        }

