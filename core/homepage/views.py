from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy

import socket
from core.homepage.models import contabilizador_visitas
from core.Auditoria.trigger_log import trigger


class IndexView(TemplateView):
    template_name = 'index.html'

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Login'
        context['login_url']= reverse_lazy('login:ingresar')

        # contabilizando las visitas 
        try:        
            nuevo1 = contabilizador_visitas(
                ip_visita_web = trigger.get_ip(self.request)
            )
            nuevo1.save()
        except Exception as e:
            pass

        return context

