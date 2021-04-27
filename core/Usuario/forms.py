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
from datetime import datetime, date
from django import forms




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

class form_crear_usuarios(ModelForm):
    user = usuario.objects.filter(borrado=0,estado=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['nombres'].widget.attrs['autofocus'] = True

    class Meta():
        model = usuario
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['primer_ingreso','fch_cambio_password','intentos_fallidos','estado','bloqueado','nombres', 'apellidos','fch_ultimo_cambio_contrasenia','fch_ultimo_login','last_login','cambiar_contrasenia','id_rol_id','fch_ingreso_labores','token','ip_ultimo_acceso','imagen_perfil','fch_modificacion', 'usuario_modificacion', 'is_active','usuario_creacion','borrado','id_rol','password','last_login','ip_ultimo_acceso','usuario_administrador','id_departamento','id_puesto']

        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                    'onkeypress': 'return nombre(event)',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'onkeypress': 'return nombre(event)',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Formado por primero nombre y apellido, ejemplo: "nombre.apellido"',
                }
            ),
            'username': TextInput(
                attrs={
                    'onkeypress': 'return usuario(event)',
                }
            ),
            'fch_ingreso_labores': DateInput(
                attrs={
                    'type': 'date',
                }
            )
            
        }

class form_editar_usuarios(ModelForm):
    user = usuario.objects.filter(borrado=0,estado=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombres'].widget.attrs['autofocus'] = True

    class Meta():
        model = usuario
        now = datetime.now()
        if len(str(now.month)) == 1:
            mes = '0' + str(now.month)
        else:
            mes = str(now.month)
        if len(str(now.day)) == 1:
            dia = '0' + str(now.day)
        else:
            dia = str(now.day)
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['primer_ingreso','username','fch_cambio_password','intentos_fallidos','fch_ultimo_cambio_contrasenia','fch_ultimo_login','last_login','cambiar_contrasenia','id_rol_id','token','ip_ultimo_acceso','imagen_perfil','fch_modificacion', 'usuario_modificacion', 'is_active','usuario_creacion','borrado','id_rol','password','last_login','ip_ultimo_acceso','usuario_administrador','id_departamento','id_puesto']

        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                    'onkeypress': 'return nombre(event)',
                    'minlength':'5',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'onkeypress': 'return nombre(event)',
                    'minlength':'5',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Formado por primero nombre y apellido, ejemplo: "nombre.apellido"',
                }
            ),
            'username': TextInput(
                attrs={
                    'onkeypress': 'return usuario(event)',
                }
            ),
            'fch_ingreso_labores': DateInput(
                attrs={
                    'type': 'date',
                    'max': str(now.year) + '-' + mes + '-' + dia,
                }
            )
            
        }

class form_primer_ingreso(forms.Form):
    polit_contrasenia = politicas_contrasenia.objects.get()
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Ingrese su nueva contraseña',
            'class': 'form-control',
            'autocomplete': 'false',
            'id': 'pass',
            'minlength': polit_contrasenia.longitud_minima_contrasenia,
            'maxlength': polit_contrasenia.longitud_maxima_contrasenia,
            'onkeypress': 'return caracteresContrasenia(event)'
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
            'onkeypress': 'return caracteresContrasenia(event)'
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

class form_roles(ModelForm):
    user = roles.objects.filter(borrado=0,estado=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta():
        model = roles
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','tiene_permisos']

        widgets = {
            'nombre': TextInput(
                attrs={
                    'onkeypress': 'return nombre(event)',
                    'placeholder': 'Ingrese el nombre del perfil',
                    'minlength': '8',
                    'id': 'id_nombres',
                }
            )
    
        }

class form_permisos(ModelForm):
    user = permisos.objects.filter(borrado=0,estado=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['pantalla'].widget.attrs['autofocus'] = True

    class Meta():
        model = permisos
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion','borrado','tiene_permisos']

        widgets = {
            'pantalla': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del perfil',
                    'onkeypress': 'return nombre(event)',
                }
            )
    
        }

class form_politicas_contrasenia(ModelForm):
    user = politicas_contrasenia.objects.all()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        #self.fields['pantalla'].widget.attrs['autofocus'] = True

    class Meta():
        model = politicas_contrasenia
        
        fields = '__all__'
        # si deseo excluir ciertos campos coloco
        exclude = ['fch_modificacion','usuario_modificacion','usuario_creacion']

        
        widgets = {
            'longitud_minima_contrasenia': NumberInput(
                attrs={
                    'min': '5',
                    'max': '10',
                }
            ),
            'longitud_maxima_contrasenia': NumberInput(
                attrs={
                    'min': '10',
                    'max': '20',
                }
            ),
            'dias_expiracion_contrasenia': NumberInput(
                attrs={
                    'min': '30',
                    'max': '360',
                }
            ),
            'intentos_sesion_maximo': NumberInput(
                attrs={
                    'min': '3',
                    'max': '10',
                }
            )
    
        }
        