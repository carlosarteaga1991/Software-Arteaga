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

class listar_politicas_contrasenia(LoginRequiredMixin,ListView):
    model = politicas_contrasenia
    template_name = 'politicas_contrasenia/listar.html'

    def get_queryset(self):
        return self.model.objects.all()

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Política de Contraseña'
        context['quitar_footer'] = 'si'
        context['titulo_lista'] = 'Política de Contraseña'
        context['mostrar_btn_crear'] = 'no'
        #context['url_salir'] = reverse_lazy('login:iniciar') 

        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Política de Contraseña'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('politicas_contrasenia:listar_politicas_contrasenia')  # esto varía
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

        return context

class editar_politicas_contrasenia(LoginRequiredMixin,UpdateView):
    model = politicas_contrasenia
    form_class = form_politicas_contrasenia
    template_name = 'politicas_contrasenia/editar.html'
    success_url = reverse_lazy('politicas_contrasenia:listar_politicas_contrasenia')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    
    def post(self, request,*args,**kwargs):
        data = {}
        try:
            # INICIO para log 
            try:
                registro_edit = politicas_contrasenia.objects.get(id_politica=self.kwargs['pk'])
                if int(registro_edit.dias_expiracion_contrasenia) != int(request.POST['dias_expiracion_contrasenia']) :
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "politicas_contrasenia",str(self.kwargs['pk']),"Editar",str(registro_edit.dias_expiracion_contrasenia),str(request.POST['dias_expiracion_contrasenia']),"dias_expiracion_contrasenia",trigger.get_ip(request),str(request.user.username))                        
                
                if int(registro_edit.longitud_maxima_contrasenia) != int(request.POST['longitud_maxima_contrasenia']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "politicas_contrasenia",str(self.kwargs['pk']),"Editar",str(registro_edit.longitud_maxima_contrasenia),str(request.POST['longitud_maxima_contrasenia']),"longitud_maxima_contrasenia",trigger.get_ip(request),str(request.user.username))                        
                
                if str(registro_edit.longitud_minima_contrasenia) != str(request.POST['longitud_minima_contrasenia']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "politicas_contrasenia",str(self.kwargs['pk']),"Editar",str(registro_edit.longitud_minima_contrasenia),str(request.POST['longitud_minima_contrasenia']),"longitud_minima_contrasenia",trigger.get_ip(request),str(request.user.username))                        
                
                if int(registro_edit.intentos_sesion_maximo) != int(request.POST['intentos_sesion_maximo']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "politicas_contrasenia",str(self.kwargs['pk']),"Editar",str(registro_edit.intentos_sesion_maximo),str(request.POST['intentos_sesion_maximo']),"intentos_sesion_maximo",trigger.get_ip(request),str(request.user.username))                        

                if str(registro_edit.complejidad_contrasenia) != str(request.POST['complejidad_contrasenia']):
                    x = trigger.guardar(str(request.user.nombres) + " " + str(request.user.apellidos), "politicas_contrasenia",str(self.kwargs['pk']),"Editar",str(registro_edit.complejidad_contrasenia),str(request.POST['complejidad_contrasenia']),"complejidad_contrasenia",trigger.get_ip(request),str(request.user.username))                        
                
                
            except Exception as e:
                pass
            # FIN para log

            registro = self.get_object()
            registro.dias_expiracion_contrasenia = int(request.POST['dias_expiracion_contrasenia'])
            registro.longitud_maxima_contrasenia = int(request.POST['longitud_maxima_contrasenia'])
            registro.longitud_minima_contrasenia = int(request.POST['longitud_minima_contrasenia'])
            registro.intentos_sesion_maximo = int(request.POST['intentos_sesion_maximo'])
            registro.complejidad_contrasenia = str(request.POST['complejidad_contrasenia'])
            registro.usuario_modificacion = int(request.user.id)
            registro.fch_modificacion = datetime.now()
            registro.save()
            
            

            return redirect('politicas_contrasenia:listar_politicas_contrasenia')
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
        context['btn_cancelar'] = reverse_lazy('politicas_contrasenia:listar_politicas_contrasenia')
        context['titulo_lista'] = 'Editar Política'
        context['icon_titulo'] = 'edit' # puede ser plus
        
        # ======INICIO Colocar en todos lo siguiente variando lo que se envía======
        context['titulo_cabecera'] = 'no'  # esto varia
        context['primera_ref'] = "si" # esto varía
        context['referencia_nombre1'] = 'Política de Contraseña'  # esto varía
        context['link_referencia_nombre1'] = reverse_lazy('politicas_contrasenia:listar_politicas_contrasenia')  # esto varía
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