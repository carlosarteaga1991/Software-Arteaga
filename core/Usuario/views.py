"""
Software-ArtPort
Fecha: 08 de abril del 2021 hora: 05:54 am
Última modificación a código
"""

from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView,UpdateView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from config.urls import *
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime,date
from core.Usuario.models import *
from core.Usuario.forms import *


class inicio_usuario(LoginRequiredMixin,TemplateView):
    template_name = 'inicio_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de Administrador'
        context['plantilla'] = 'Inicio'
        context['tiempo_AM_PM'] = datetime.today().strftime("%p")

        # Colocar en todos lo siguiente variando lo que se envía
        context['link_home'] = reverse_lazy('usuario:inicio')
        context['referencia_nombre'] = 'Dashboard' # esto varía 
        context['link_referencia_nombre'] = reverse_lazy('usuario:inicio')  # esto varía

        context['quitar_footer'] = 'no'

        # INICIO VERIFICACIÓN DE PERMISOS 
        #context['permisos'] = asignar_permiso().metodo_permiso(28,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS

        # INICIO PARA RECORDATORIOS HEADER
        #context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER
        #context['cont_promesa'] = alertas().promesas(self.request.user)
        #context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER

        return context

class editar_perfil_usuario(LoginRequiredMixin,UpdateView):
    model = usuario
    form_class = form_perfil_usuario
    template_name = 'usuario/editar_perfil.html'
    success_url = reverse_lazy('usuario:inicio')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def get_object(self, get_queryset=None):
        return self.request.user
    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.email = request.POST['email']
            registro.nombres = request.POST['nombres']
            registro.apellidos = request.POST['apellidos']
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.imagen_perfil = request.FILES['imagen_perfil']
            registro.save()
            return redirect('usuario:inicio')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('usuario:inicio')
        context['titulo_lista'] = 'Editar Perfil de '

        # Colocar en todos lo siguiente variando lo que se envía
        context['titulo_cabecera'] = 'no' # esto varia
        context['link_home'] = reverse_lazy('usuario:inicio')
        context['referencia_nombre'] = 'Editar Perfil' # esto varía 
        context['link_referencia_nombre'] = reverse_lazy('usuario:editar_perfil')  # esto varía
        
        """
        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'actualizar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
        # FIN VERIFICACIÓN DE PERMISOS
        

        # INICIO PARA RECORDATORIOS HEADER
        context['cont_alerta'] = alertas().recordatorios(self.request.user)
        # FIN PARA RECORDATORIOS HEADER

        # INICIO PARA PROMESAS HEADER 
        context['cont_promesa'] = alertas().promesas(self.request.user)
        context['cont_total'] = alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)
        # FIN PARA PROMESAS HEADER
        """

        return context