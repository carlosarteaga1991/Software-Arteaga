

from django.contrib import admin

from core.RRHH.models import *
from core.Usuario.models import usuario

#para agregar filtros en el panel de administración
class filtroDepartamentos(admin.ModelAdmin):
    list_display = ("nombre","usuario_creacion","estado") # esto para mostrar sólo algunos campos
    # y se agrega al admin.site.register
    # y para agregar los filtros de busqueda se colocan los campos q se desan hacer búsqueda
    search_fields = ("nombre","usuario_creacion","estado")

admin.site.register(usuario)

admin.site.register(puestos)
admin.site.register(departamentos, filtroDepartamentos)
admin.site.register(empresas)