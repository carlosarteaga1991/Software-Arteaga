"""
Software-ArtPort
Fecha: 24 de abril del 2021
Última modificación a código
"""

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import FormView, ListView, UpdateView,DeleteView, TemplateView
from django.urls import reverse_lazy
from config.urls import *
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, date
from core.Usuario.models import *
from core.Usuario.forms import *
from core.RRHH.models import *

# Importar para alimentar log
from core.Auditoria.trigger_log import trigger

class listar_roles(LoginRequiredMixin,ListView):
    model = roles
    template_name = 'perfiles_roles/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Perfiles de usuario'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Perfiles existentes'
        context['create_url'] = reverse_lazy('perfiles_roles:crear_perfiles_roles')
        #context['url_salir'] = reverse_lazy('login:iniciar')

        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Perfiles de Usuario'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')  # esto varía
        context['color1'] = 'gray'
        context['segunda_ref'] = "no" # esto varía
        context['referencia_nombre2'] = ''  # esto varía
        context['link_referencia_nombre2'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')  # esto varía
        context['color2'] = ''
        #mes
        if len(str(self.request.user.fch_modificacion.month)) == 1:
            mes_edit_perfil = '0' + str(self.request.user.fch_modificacion.month)
        else:
            mes_edit_perfil = str(self.request.user.fch_modificacion.month)
        #dia
        if len(str((self.request.user.fch_modificacion.day))) == 1:
            dia_edit_perfil = '0' + str(self.request.user.fch_modificacion.day)
        else:
            dia_edit_perfil = str(self.request.user.fch_modificacion.day)
        context['fch_modificacion_perfil'] = str(self.request.user.fch_modificacion.year) + "/" + str(mes_edit_perfil) + "/" + str(dia_edit_perfil)
        context['fch_modificacion_password'] = self.request.user.fch_ultimo_cambio_contrasenia[0:10]
        context['link_home'] = reverse_lazy('usuario:inicio')
        # ======FIN Colocar en todos lo siguiente variando lo que se envía======

        """
        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(1,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
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

class crear_roles(LoginRequiredMixin,CreateView):
    model = roles
    form_class = form_roles
    template_name = 'perfiles_roles/crear.html'
    success_url = reverse_lazy('perfiles_roles:listar_perfiles_roles')

    
    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)

        try:
            #if form.is_valid():
                

                nuevo = roles(
                    nombre = request.POST['nombre'],
                    fch_creacion = datetime.now(),
                    usuario_creacion = int(request.user.id)
                )
                nuevo.save()
                # INICIO para log
                try:
                    #if form.is_valid():
                    id_rol_new = roles.objects.get(nombre=str(request.POST['nombre']))
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "roles",str(id_rol_new.id_rol),"Crear","",str(request.POST['nombre']),"nombre de perfil",trigger.get_ip(request),str(request.user.username))                        

                except Exception as e:
                    pass
                # FIN para log
                return redirect('perfiles_roles:listar_perfiles_roles') 
            #else:
                
        except Exception as e:
            #return render(request, self.template_name, {'form':form, 'quitar_footer': 'si','ya_existe': 'si', 'titulo_lista': 'Ingrese datos del nuevo perfil','plantilla': 'Crear'})
            self.object = None
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['nombre_post'] = request.POST['nombre']
            return render(request, self.template_name,context)
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('perfiles_roles:listar_perfiles_roles') 
        context['titulo_lista'] = 'Ingrese datos del nuevo perfil'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'
        #context['formguardarusuario'] = form_usuarios()

        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Perfiles de Usuario'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')  # esto varía
        context['color1'] = ''
        context['segunda_ref'] = "si" # esto varía
        context['referencia_nombre2'] = 'Crear'  # esto varía
        context['link_referencia_nombre2'] = reverse_lazy('perfiles_roles:crear_perfiles_roles')  # esto varía
        context['color2'] = 'gray'
        #mes
        if len(str(self.request.user.fch_modificacion.month)) == 1:
            mes_edit_perfil = '0' + str(self.request.user.fch_modificacion.month)
        else:
            mes_edit_perfil = str(self.request.user.fch_modificacion.month)
        #dia
        if len(str((self.request.user.fch_modificacion.day))) == 1:
            dia_edit_perfil = '0' + str(self.request.user.fch_modificacion.day)
        else:
            dia_edit_perfil = str(self.request.user.fch_modificacion.day)
        context['fch_modificacion_perfil'] = str(self.request.user.fch_modificacion.year) + "/" + str(mes_edit_perfil) + "/" + str(dia_edit_perfil)
        context['fch_modificacion_password'] = self.request.user.fch_ultimo_cambio_contrasenia[0:10]
        context['link_home'] = reverse_lazy('usuario:inicio')
        # ======FIN Colocar en todos lo siguiente variando lo que se envía======
       
        """
        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(1,'crear',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
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

class editar_roles(LoginRequiredMixin,UpdateView):
    model = roles
    form_class = form_roles
    template_name = 'perfiles_roles/editar.html'
    success_url = reverse_lazy('perfiles_roles:listar_perfiles_roles')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    
    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        try:
            # INICIO para log
            try:
                #if form.is_valid():
                    rol_edit = roles.objects.get(id_rol = self.kwargs['pk'])

                    if str(rol_edit.estado) != str(request.POST['estado']) :
                        x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "roles",str(rol_edit.id_rol),"Modificar",str(rol_edit.estado),str(request.POST['estado']),"estado",trigger.get_ip(request),str(request.user.username))    

                    if str(rol_edit.nombre) != str(request.POST['nombre']) :
                        x4 = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "roles",str(rol_edit.id_rol),"Modificar",str(rol_edit.nombre),str(request.POST['nombre']),"nombre rol",trigger.get_ip(request),str(request.user.username))                        
                    

            except Exception as e:
                pass
            # FIN para log
            registro = self.get_object()
            registro.nombre = request.POST['nombre']
            registro.estado = request.POST['estado']
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('perfiles_roles:listar_perfiles_roles')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')
        context['titulo_lista'] = 'Editar Perfil/Rol de Usuario'

        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Perfiles de Usuario'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')  # esto varía
        context['color1'] = ''
        context['segunda_ref'] = "si" # esto varía
        context['referencia_nombre2'] = 'Editar'  # esto varía
        context['link_referencia_nombre2'] = ''  # esto varía
        context['color2'] = 'gray'
        #mes
        if len(str(self.request.user.fch_modificacion.month)) == 1:
            mes_edit_perfil = '0' + str(self.request.user.fch_modificacion.month)
        else:
            mes_edit_perfil = str(self.request.user.fch_modificacion.month)
        #dia
        if len(str((self.request.user.fch_modificacion.day))) == 1:
            dia_edit_perfil = '0' + str(self.request.user.fch_modificacion.day)
        else:
            dia_edit_perfil = str(self.request.user.fch_modificacion.day)
        context['fch_modificacion_perfil'] = str(self.request.user.fch_modificacion.year) + "/" + str(mes_edit_perfil) + "/" + str(dia_edit_perfil)
        context['fch_modificacion_password'] = self.request.user.fch_ultimo_cambio_contrasenia[0:10]
        context['link_home'] = reverse_lazy('usuario:inicio')
        # ======FIN Colocar en todos lo siguiente variando lo que se envía======

        """
        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(1,'actualizar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
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

class borrar_roles(LoginRequiredMixin,DeleteView):
    model = roles
    template_name = 'perfiles_roles/borrar.html'
    success_url = reverse_lazy('perfiles_roles:listar_perfiles_roles')

    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.borrado = 1
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            # INICIO para log
            try:
                id_borrado = roles.objects.get(id_rol = int(self.kwargs['pk']))
                x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "roles", id_borrado.id_rol,"Borrar", "0","1","borrado",trigger.get_ip(request), str(request.user.username))          

            except Exception as e:
                pass
            # FIN para log
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Eliminar'
        context['btn_cancelar'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')
        context['list_url'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')
        context['quitar_footer'] = 'si'
        context['url_salir'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')
        context['titulo_lista'] = 'Eliminar Perfil/Rol de Usuario'

        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Perfiles de Usuario'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('perfiles_roles:listar_perfiles_roles')  # esto varía
        context['color1'] = ''
        context['segunda_ref'] = "si" # esto varía
        context['referencia_nombre2'] = 'Borrar'  # esto varía
        context['link_referencia_nombre2'] = ''  # esto varía
        context['color2'] = 'gray'
        #mes
        if len(str(self.request.user.fch_modificacion.month)) == 1:
            mes_edit_perfil = '0' + str(self.request.user.fch_modificacion.month)
        else:
            mes_edit_perfil = str(self.request.user.fch_modificacion.month)
        #dia
        if len(str((self.request.user.fch_modificacion.day))) == 1:
            dia_edit_perfil = '0' + str(self.request.user.fch_modificacion.day)
        else:
            dia_edit_perfil = str(self.request.user.fch_modificacion.day)
        context['fch_modificacion_perfil'] = str(self.request.user.fch_modificacion.year) + "/" + str(mes_edit_perfil) + "/" + str(dia_edit_perfil)
        context['fch_modificacion_password'] = self.request.user.fch_ultimo_cambio_contrasenia[0:10]
        context['link_home'] = reverse_lazy('usuario:inicio')
        # ======FIN Colocar en todos lo siguiente variando lo que se envía======

        """
        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(1,'borrar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
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