from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from core.Usuario.forms import *
from django.urls import reverse_lazy
from core.RRHH.models import *
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from core.Usuario.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Importar para alimentar log
from core.Auditoria.trigger_log import trigger

class listar_permisos(LoginRequiredMixin,ListView):
    model = permisos
    template_name = 'permisos/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(borrado=0)

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Permisos'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Permisos existentes'
        context['create_url'] = reverse_lazy('permisos:crear_permisos')
        #context['url_salir'] = reverse_lazy('login:iniciar') 

        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Permisos'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('permisos:listar_permisos')  # esto varía
        context['color1'] = 'gray'
        context['segunda_ref'] = "no" # esto varía
        context['referencia_nombre2'] = 'Borrar'  # esto varía
        context['link_referencia_nombre2'] = ''  # esto varía
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
        context['permisos'] = asignar_permiso().metodo_permiso(2,'ver',int(self.request.user.id_rol_id),self.request.user.usuario_administrador)
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

class crear_permisos(LoginRequiredMixin,CreateView):
    model = permisos
    form_class = form_permisos
    template_name = 'permisos/crear.html'
    success_url = reverse_lazy('permisos:listar_permisos')

    
    def post(self, request,*args,**kwargs):
        data = {}
        form = self.form_class(request.POST)
        condicion_pantalla = permisos.objects.filter(borrado=0,estado=1,id_rol_id=int(request.POST['id_rol']))
        x = 0
        for  p in condicion_pantalla:
            if p.pantalla_id == int(request.POST['pantalla']):
                x = 1

        try:
            #for p in condicion_pantalla:
                if x == 1:
                    #rol = roles.objects.filter(borrado=0,estado=1) 
                    #pantalla = pantallas.objects.all()
                    #return render(request,self.template_name, {'pantalla':pantalla,'ya_existe': 'si','form':form,'rol':rol, 'quitar_footer': 'si', 'titulo_lista': 'Seleccione los datos del nuevo permiso','plantilla': 'Crear'})
                    self.object = None
                    context = self.get_context_data(**kwargs)
                    context['form'] = form
                    context['ya_existe'] =  'si'
                    return render(request, self.template_name,context)
                else:
                    nuevo = permisos(
                        id_rol_id = int(request.POST['id_rol']),
                        pantalla_id = int(request.POST['pantalla']),
                        ver = int(request.POST['ver']),
                        actualizar = int(request.POST['actualizar']),
                        crear = int(request.POST['crear']),
                        borrar = int(request.POST['borrar']),
                        fch_creacion = datetime.now(),
                        usuario_creacion = int(request.user.id)
                    )
                    nuevo.save()
                    # INICIO para log 
                    try:
                        id_permiso_new = permisos.objects.get(id_rol_id=int(request.POST['id_rol']),pantalla_id=int(request.POST['pantalla']))
                        x1 = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(id_permiso_new.id_permiso),"Crear","",str(request.POST['id_rol']),"tipo de permiso",trigger.get_ip(request),str(request.user.username))                        

                    except Exception as e:
                        pass
                    # FIN para log
                    return redirect('permisos:listar_permisos')
        except Exception as e:
            #return render(request, self.template_name, {'form':form, 'quitar_footer': 'si', 'titulo_lista': 'Seleccione los datoxxxs del nuevo permiso','plantilla': 'Crear'})
            self.object = None
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name,context)
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Crear'
        context['btn_cancelar'] = reverse_lazy('permisos:listar_permisos')
        context['titulo_lista'] = 'Seleccione los datos del nuevo permiso'
        context['quitar_footer'] = 'si'
        context['tipo'] = 'nuevo'
        rol = roles.objects.filter(borrado=0,estado=1)
        context['rol'] = rol
        pantalla = pantallas.objects.filter(estado=1)
        context['pantalla'] = pantalla
        #context['formguardarusuario'] = form_usuarios()

        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Permisos'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('permisos:listar_permisos')  # esto varía
        context['color1'] = ''
        context['segunda_ref'] = "si" # esto varía
        context['referencia_nombre2'] = 'Crear'  # esto varía
        context['link_referencia_nombre2'] = reverse_lazy('permisos:crear_permisos')  # esto varía
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
       
       
       
        return context

class editar_permisos(LoginRequiredMixin,UpdateView):
    model = permisos
    form_class = form_permisos
    template_name = 'permisos/editar.html'
    success_url = reverse_lazy('permisos:listar_permisos')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            # INICIO para log 
            try:
                registro_edit = permisos.objects.get(id_permiso=self.kwargs['pk'])
                if int(registro_edit.id_rol_id) != int(request.POST['id_rol']) :
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(self.kwargs['pk']),"Editar",str(registro_edit.id_rol_id),str(request.POST['id_rol']),"id rol",trigger.get_ip(request),str(request.user.username))                        
                
                if int(registro_edit.pantalla_id) != int(request.POST['pantalla']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(self.kwargs['pk']),"Editar",str(registro_edit.pantalla_id),str(request.POST['pantalla']),"id pantalla",trigger.get_ip(request),str(request.user.username))                        
                
                if str(registro_edit.estado) != str(request.POST['estado']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(self.kwargs['pk']),"Editar",str(registro_edit.estado),str(request.POST['estado']),"estado",trigger.get_ip(request),str(request.user.username))                        
                
                if int(registro_edit.ver) != int(request.POST['ver']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(self.kwargs['pk']),"Editar",str(registro_edit.ver),str(request.POST['ver']),"ver",trigger.get_ip(request),str(request.user.username))                        

                if int(registro_edit.actualizar) != int(request.POST['actualizar']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(self.kwargs['pk']),"Editar",str(registro_edit.actualizar),str(request.POST['actualizar']),"actualizar",trigger.get_ip(request),str(request.user.username))                        
                
                if int(registro_edit.crear) != int(request.POST['crear']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(self.kwargs['pk']),"Editar",str(registro_edit.crear),str(request.POST['crear']),"crear",trigger.get_ip(request),str(request.user.username))                        

                if int(registro_edit.borrar) != int(request.POST['borrar']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(self.kwargs['pk']),"Editar",str(registro_edit.borrar),str(request.POST['borrar']),"borrar",trigger.get_ip(request),str(request.user.username))                        

               
            except Exception as e:
                pass
            # FIN para log

            registro = self.get_object()
            registro.id_rol_id = request.POST['id_rol']
            registro.pantalla_id = request.POST['pantalla']
            registro.estado = request.POST['estado']
            registro.ver = int(request.POST['ver'])
            registro.actualizar = int(request.POST['actualizar'])
            registro.crear = int(request.POST['crear'])
            registro.borrar = int(request.POST['borrar'])
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            
            

            return redirect('permisos:listar_permisos')
        except Exception as e:
            self.object = None
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name,context)
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Editar'
        context['quitar_footer'] = 'si'
        context['btn_cancelar'] = reverse_lazy('permisos:listar_permisos')
        context['titulo_lista'] = 'Editar permiso'
        rol = roles.objects.filter(borrado=0,estado=1)
        context['rol'] = rol
        permiso = permisos.objects.filter(id_permiso = int(self.kwargs['pk']))
        pantalla = pantallas.objects.all()
        context['iterar_pantalla'] = pantalla
        for x in permiso:
            context['pantalla'] = x.pantalla_id
            context['id_rol'] = x.id_rol_id
            context['ver_select'] = x.ver
            context['actualizar'] = x.actualizar
            context['crear'] = x.crear
            context['borrar'] = x.borrar
        
        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Permisos'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('permisos:listar_permisos')  # esto varía
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
        
        
        return context

class borrar_permisos(LoginRequiredMixin,DeleteView):
    model = permisos
    template_name = 'permisos/borrar.html'
    success_url = reverse_lazy('permisos:listar_permisos')

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
                registro_edit = permisos.objects.get(id_permiso=self.kwargs['pk'])
                if str(registro_edit.borrado) == '1' :
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "permisos",str(self.kwargs['pk']),"Borrar","0","1","borrar",trigger.get_ip(request),str(request.user.username))                        
                
            except Exception as e:
                pass
            # FIN para log

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Eliminar'
        context['btn_cancelar'] = reverse_lazy('permisos:listar_permisos')
        context['list_url'] = reverse_lazy('permisos:listar_permisos')
        context['quitar_footer'] = 'si'
        #context['url_salir'] = reverse_lazy('login:iniciar')
        context['titulo_lista'] = 'Eliminar permiso'
        context['borrar_titulo'] = 'de permiso que pertenece a ' + str(roles.objects.get(id_rol=permisos.objects.get(id_permiso=self.kwargs['pk']).id_rol_id).nombre)
        context['borrar_permiso'] = pantallas.objects.get(id_pantalla=permisos.objects.get(id_permiso=self.kwargs['pk']).pantalla_id).nombre

        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Permisos'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('permisos:listar_permisos')  # esto varía
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


        return context