
from django.db import models
from django.forms import model_to_dict
from core.Usuario.models import * 


class log(models.Model):
    id_log = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=50,blank=True,null=True)
    nombre_tabla = models.CharField(max_length=60)
    fecha = models.DateTimeField(auto_now_add=True)
    id_registro = models.IntegerField(blank=True,null=True)
    tipo_accion = models.CharField(max_length=50,blank=True,null=True)
    Dato_anterior = models.CharField(max_length=400,blank=True)
    Dato_despues = models.CharField(max_length=400,blank=True)
    campo_afectado = models.CharField(max_length=50,blank=True)
    ip_accion = models.CharField(max_length=50,blank=True,null=True)
    user_log = models.CharField(max_length=70,blank=True,null=True)

    def __str__(self):
        return self.nombre_tabla
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Bitácoras'
        ordering = ['fecha']

class historial_contrasenia(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(usuario,on_delete=models.PROTECT,verbose_name="Usuario")
    fecha = models.DateTimeField(auto_now_add=True)
    contrasenia = models.CharField(max_length=128,blank=True,null=True)
    ip_accion = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.nombre_tabla
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'Historial Contraseñas'
        ordering = ['fecha']