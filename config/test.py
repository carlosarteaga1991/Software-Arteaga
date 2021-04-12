from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, RedirectView,TemplateView

import config.settings as setting
from config import settings
from core.login.forms import *
from core.Usuario.models import *


class vista_prueba(TemplateView):
    template_name = 'reset_send_email.html'

    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'prueba'
        context['btn_cancelar'] = reverse_lazy('pagina_web')
        context['login_url']= reverse_lazy('login:ingresar')
        return context