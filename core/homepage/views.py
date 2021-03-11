from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantilla'] = 'Login'
        #context['login_url']= reverse_lazy('login:iniciar')
        return context
