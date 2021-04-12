"""
Software-ArtPort
Fecha: 08 de abril del 2021 hora: 05:54 am
Última modificación a código
"""

from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from config.urls import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import *

# Importanto para el formulario a usar
from core.login.forms import *

# para enviar correo
from config.settings import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from core.Usuario.models import *

class login(LoginView):
    template_name = 'login.html'

    # importante se sobre escribe este método para verificar si está loggeado y si es así redireccionarlo
    # importante recordar q esa URL se configura en setting .py 
    # usando LOGIN_REDIRECT_URL = '/cobros/departamento/' si desea volver a loggerse

    def dispatch(self, request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('usuario:inicio')
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Login'
        context['btn_cancelar'] = reverse_lazy('pagina_web')
        context['titulo_lista'] = 'Iniciar Sesión'
        context['login_url']= reverse_lazy('login:ingresar')
        context['recuperar_password']= reverse_lazy('login:resetear_password')
        
        return context

# se hace con FormView para validar si existe el usuario
class resetear_contrasenia(FormView):
    form_class = form_reseteo_contrasenia
    template_name = 'recuperar_contrasenia.html'
    success_url = reverse_lazy('login:ingresar')

    @method_decorator(csrf_exempt)
    def dispatch(self, request,*args,**kwargs):
        # en caso que el usuario esté loggeado mandar a perfil
        if request.user.is_authenticated:
            return redirect('usuario:inicio')
        return super().dispatch(request,*args,**kwargs)

    def send_email_reset_pwd(self, usuario_email):
        data = {}
        try:
            mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

            email_to = usuario_email.email
            mensaje = MIMEMultipart()
            mensaje['From'] = EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de Contraseña'

            content = render_to_string('reset_send_email.html', {
                'usuario': usuario_email,#usuario.objects.get(pk=1),
                'link_resetpwd': 'https://www.youtube.com/',
                'link_home': ''
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

    # procedemos a sobre escribir el método POST
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = form_reseteo_contrasenia(request.POST)  # le enviamos la información que llega del POST y la guardamos en una variable
            if form.is_valid():
                #print(request.POST) # probando si llega el usuario
                usuario_email = form.get_user()
                data = self.send_email_reset_pwd(usuario_email)
                data['exitoso'] = 'si'
            else:
                data['error'] = form.errors
            #si se está ysando CreateView colocar
            self.object = None
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['errores']=form.errors
            context['exitoso'] = data['exitoso']
        except Exception as e:
            data['error'] = str(e)
        return render(request, self.template_name, context)
        #return JsonResponse(data, safe=False)

    def form_valid(self, form):
        pass
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Reseteo de Contraseña'
        context['btn_cancelar'] = reverse_lazy('pagina_web')
        context['login_url']= reverse_lazy('login:ingresar')
        
        return context
