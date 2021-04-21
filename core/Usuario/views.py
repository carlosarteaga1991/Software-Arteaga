"""
Software-ArtPort
Fecha: 08 de abril del 2021 hora: 05:54 am
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


class inicio_usuario(LoginRequiredMixin, TemplateView):
    template_name = 'inicio_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de Administrador'
        context['plantilla'] = 'Inicio'
        context['tiempo_AM_PM'] = datetime.today().strftime("%p")

        # Colocar en todos lo siguiente variando lo que se envía
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
        context['referencia_nombre'] = 'Dashboard'  # esto varía
        context['link_referencia_nombre'] = reverse_lazy('usuario:inicio')  # esto varía
        if self.request.user.estado == '1':
            estado = 'Activo'
        else:
            estado='Inactivo'
        context['estado'] = estado

        # Obteniendo datos del usuario loggeado
        departameto = departamentos.objects.get(id_departamento=self.request.user.id_departamento)
        puesto = puestos.objects.get(id_puesto=self.request.user.id_puesto)
        context['departamento'] = departameto
        context['puesto'] = puesto

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


class editar_perfil_usuario(LoginRequiredMixin, UpdateView):
    model = usuario
    form_class = form_perfil_usuario
    template_name = 'usuario/editar_perfil.html'
    success_url = reverse_lazy('usuario:inicio')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, get_queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            """
            registro = self.get_object()
            registro.email = request.POST['email']
            registro.nombres = request.POST['nombres']
            registro.apellidos = request.POST['apellidos']
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.imagen_perfil = request.FILES['imagen_perfil']
            registro.save()
            """
            # INICIO para log
            try:
                if str(request.user.email) != str(request.POST['email']) :
                    x4 = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "usuario",str(request.user.id),"Modificar",str(request.user.email),str(request.POST['email']),"correo",trigger.get_ip(request),str(request.user.username))                        
                if str(request.user.nombres.strip()) != str(request.POST['nombres'].strip()):

                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "usuario",str(request.user.id),"Modificar",str(request.user.nombres),str(request.POST['nombres']),"nombres",trigger.get_ip(request),str(request.user.username))

                if str(request.user.apellidos.strip()) != request.POST['apellidos'].strip():
                    x2 = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "usuario",str(request.user.id),"Modificar",str(request.user.apellidos),str(request.POST['apellidos']),"apellidos",trigger.get_ip(request),str(request.user.username))                   

                if str(request.user.imagen_perfil) != str(request.FILES['imagen_perfil']):
                    x3 = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "usuario",str(request.user.id),"Modificar",str(request.user.imagen_perfil),str(request.FILES['imagen_perfil']),"imagen_perfil",trigger.get_ip(request),str(request.user.username))                        

            except Exception as e:
                pass
            # FIN para log
            registro = self.get_object()
            registro.fch_modificacion = datetime.now()
            registro.save()

            form = self.get_form()
            data = form.save()
            
            return redirect('usuario:inicio')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar Perfil'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('usuario:inicio')
        context['titulo_lista'] = 'Editar Perfil de '

        # INICIO Colocar en todos lo siguiente variando lo que se envía
        context['titulo_cabecera'] = 'no'  # esto varia
        context['link_home'] = reverse_lazy('usuario:inicio')
        context['referencia_nombre'] = 'Editar Perfil'  # esto varía
        context['link_referencia_nombre'] = reverse_lazy('usuario:editar_perfil')  # esto varía
        #  en todos lo siguiente variando lo que se envía
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
        # FIN Colocar en todos lo siguiente variando lo que se envía


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


class cambiar_password_usuario(LoginRequiredMixin, FormView):
    model = usuario
    form_class = PasswordChangeForm
    template_name = 'usuario/cambiar_password.html'
    success_url = reverse_lazy('inicio_sesion')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, get_queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        polit_contrasenia = politicas_contrasenia.objects.get()
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'

        form.fields['old_password'].widget.attrs['autocomplete'] = 'off'
        form.fields['new_password1'].widget.attrs['autocomplete'] = 'off'
        form.fields['new_password2'].widget.attrs['autocomplete'] = 'off'

        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'

        form.fields['new_password2'].widget.attrs['onkeyup'] = 'validarContrasenia_loggin(value)'
        form.fields['new_password2'].widget.attrs['minlength'] = polit_contrasenia.longitud_minima_contrasenia
        form.fields['new_password2'].widget.attrs['maxlength'] = polit_contrasenia.longitud_maxima_contrasenia
        form.fields['new_password2'].widget.attrs['onkeypress'] = 'return caracteresContrasenia(event)'

        form.fields['new_password1'].widget.attrs['minlength'] = polit_contrasenia.longitud_minima_contrasenia
        form.fields['new_password1'].widget.attrs['maxlength'] = polit_contrasenia.longitud_maxima_contrasenia
        form.fields['new_password1'].widget.attrs['onkeypress'] = 'return caracteresContrasenia(event)'

        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            form.fields['old_password'].widget.attrs['value'] = request.POST['old_password']
            form.fields['new_password1'].widget.attrs['value'] = request.POST['new_password1']
            form.fields['new_password2'].widget.attrs['value'] = request.POST['new_password2']
            if form.is_valid():
                form.save()
                registro = self.get_object()
                fch = datetime.now()
                #mes
                if len(str(fch.month)) == 1:
                    mes = '0' + str(fch.month)
                else:
                    mes = str(fch.month)
                #dia
                if len(str(fch.day)) == 1:
                    dia = '0' + str(fch.day)
                else:
                    dia = str(fch.day)
                registro.fch_ultimo_cambio_contrasenia = str(fch.year) + '/' + str(mes) + '/' + str(dia) + '  ' + datetime.today().strftime("%H:%M %p")
                registro.save()
                # INICIO para log
                try:
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "usuario",str(request.user.id),"Edición Contraseña",str(request.user.password),make_password(request.POST['new_password2']),"password",trigger.get_ip(request),str(request.user.username))
                    x2 = trigger.guardar_historial_pass(make_password(request.POST['new_password2']),trigger.get_ip(request),int(request.user.id))
                except Exception as e:
                    pass
                # FIN para log
                #update_session_auth_hash(request, form.user)
                return redirect('/login/')
            else:
                data['error'] = form.errors
                polit_contrasenia = politicas_contrasenia.objects.get()
                form.fields['old_password'].widget.attrs['class'] = 'form-control'
                form.fields['new_password1'].widget.attrs['class'] = 'form-control'
                form.fields['new_password2'].widget.attrs['class'] = 'form-control'

                form.fields['old_password'].widget.attrs['autocomplete'] = 'off'
                form.fields['new_password1'].widget.attrs['autocomplete'] = 'off'
                form.fields['new_password2'].widget.attrs['autocomplete'] = 'off'

                form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
                form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
                form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'

                form.fields['new_password2'].widget.attrs['onkeyup'] = 'validarContrasenia_loggin(value)'
                form.fields['new_password2'].widget.attrs['minlength'] = polit_contrasenia.longitud_minima_contrasenia
                form.fields['new_password2'].widget.attrs['maxlength'] = polit_contrasenia.longitud_maxima_contrasenia
                form.fields['new_password2'].widget.attrs['onkeypress'] = 'return caracteresContrasenia(event)'

                form.fields['new_password1'].widget.attrs['minlength'] = polit_contrasenia.longitud_minima_contrasenia
                form.fields['new_password1'].widget.attrs['maxlength'] = polit_contrasenia.longitud_maxima_contrasenia
                form.fields['new_password1'].widget.attrs['onkeypress'] = 'return caracteresContrasenia(event)'
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return render(request, self.template_name,context) 
                #return render(request, self.template_name, {'action': 'cambiar_contrasenia', 'form': form, 'quitar_footer': 'si', 'titulo_lista': 'Editar Contraseña de Usuario', 'plantilla': 'Editar Contraseña', 'permisos': asignar_permiso().metodo_permiso(3, 'actualizar', int(self.request.user.id_rol_id), self.request.user.usuario_administrador), 'cont_alerta': alertas().recordatorios(self.request.user), 'cont_promesa': alertas().promesas(self.request.user), 'cont_total': alertas().promesas(self.request.user) + alertas().recordatorios(self.request.user)})

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar Contraseña'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('usuario:inicio')
        context['titulo_lista'] = 'Editar Contraseña de '

        # Colocar en todos lo siguiente variando lo que se envía
        # Puede ser fas fa-plus (para agregar) fas fa-trash (para borrar) fas fa-edit (para editar)
        context['logo_titulo'] = 'fas fa-edit'
        context['titulo_cabecera'] = 'no'  # esto varia
        context['link_home'] = reverse_lazy('usuario:inicio')
        context['referencia_nombre'] = 'Editar Contraseña'  # esto varía
        context['link_referencia_nombre'] = reverse_lazy('usuario:editar_contrasenia')  # esto varía
        # Colocar en todos lo siguiente variando lo que se envía
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

class listar_usuarios(LoginRequiredMixin,ListView):
    model = usuario
    template_name = 'usuario/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0,usuario_administrador='0')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Usuarios'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Usuarios existentes'
        #context['create_url'] = reverse_lazy('crear_usuarios')
        #context['url_salir'] = reverse_lazy('login:iniciar')
        departamento = departamentos.objects.filter(borrado=0,estado=1)
        puesto = puestos.objects.filter(borrado=0,estado=1)
        context['departamento'] = departamento
        context['puesto'] = puesto

        # INICIO Colocar en todos lo siguiente variando lo que se envía
        context['titulo_cabecera'] = 'no'  # esto varia
        context['link_home'] = reverse_lazy('usuario:inicio')
        context['referencia_nombre'] = 'Lista de Usuarios'  # esto varía
        context['link_referencia_nombre'] = reverse_lazy('usuario:listar_usuarios')  # esto varía
        #  en todos lo siguiente variando lo que se envía
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
        # FIN Colocar en todos lo siguiente variando lo que se envía

        """
        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
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

class editar_usuario(LoginRequiredMixin,UpdateView):
    model = usuario
    form_class = form_editar_usuarios
    template_name = 'usuario/editar.html'
    success_url = reverse_lazy('usuario:listar_usuarios')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            registro = self.get_object()
            registro.id_puesto = int(request.POST['id_puesto'])
            registro.id_departamento = int(request.POST['id_departamento'])
            registro.username = request.POST['username']
            registro.email = request.POST['email']
            registro.nombres = request.POST['nombres']
            registro.apellidos = request.POST['apellidos']
            registro.estado = request.POST['estado']
            registro.id_rol_id = request.POST['id_rol']
            if request.POST['cambiar_contrasenia'] == '1':
                registro.cambiar_contrasenia = request.POST['cambiar_contrasenia']
                registro.password = make_password(request.POST['username'])
            else:
                registro.cambiar_contrasenia = request.POST['cambiar_contrasenia']
            registro.bloqueado = request.POST['bloqueado']
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            return redirect('listar_usuarios')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('usuario:listar_usuarios')
        context['titulo_lista'] = 'Editar usuario:'
        departamento = departamentos.objects.filter(borrado=0,estado=1)
        puesto = puestos.objects.filter(borrado=0,estado=1)
        context['departamento'] = departamento
        context['puesto'] = puesto
        user = usuario.objects.filter(borrado=0, id = self.kwargs['pk'])
        z = 0
        zz = 0
        zzz = 0
        for c in user:
            z = c.id_departamento
            zz = c.id_puesto
            zzz = c.id_rol_id
        context['seleccionar_dep'] = z
        context['seleccionar_puesto'] = zz
        context['seleccionar_rol'] = zzz
        rol = roles.objects.filter(borrado=0,estado=1,tiene_permisos='Si')
        context['rol'] = rol
        user1 = usuario.objects.get(borrado=0, id = self.kwargs['pk'])
        context['nombre_usuario'] = user1.username

        # INICIO Colocar en todos lo siguiente variando lo que se envía
        context['titulo_cabecera'] = 'no'  # esto varia
        context['link_home'] = reverse_lazy('usuario:inicio')
        context['referencia_nombre'] = 'Editar de Usuario'  # esto varía
        #context['link_referencia_nombre'] = reverse_lazy('usuario:editar_usuarios')  # esto varía
        #  en todos lo siguiente variando lo que se envía
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
        # FIN Colocar en todos lo siguiente variando lo que se envía

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

class borrar_usuario(LoginRequiredMixin,DeleteView):
    model = usuario
    template_name = 'usuario/borrar.html'
    success_url = reverse_lazy('usuario:listar_usuarios')

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
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Eliminar'
        context['btn_cancelar'] = reverse_lazy('usuario:listar_usuarios')
        context['list_url'] = reverse_lazy('usuario:listar_usuarios')
        context['quitar_footer'] = 'si'
        #context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar usuario'

        # INICIO Colocar en todos lo siguiente variando lo que se envía
        context['titulo_cabecera'] = 'no'  # esto varia
        context['link_home'] = reverse_lazy('usuario:inicio')
        context['referencia_nombre'] = 'Borrar Usuario'  # esto varía
        #context['link_referencia_nombre'] = reverse_lazy('usuario:borrar_usuarios')  # esto varía
        #  en todos lo siguiente variando lo que se envía
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
        # FIN Colocar en todos lo siguiente variando lo que se envía

        """
        # INICIO VERIFICACIÓN DE PERMISOS
        context['permisos'] = asignar_permiso().metodo_permiso(3,'borrar',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
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