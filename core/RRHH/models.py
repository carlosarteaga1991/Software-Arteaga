"""
Software-ArtPort
Fecha: 06 de abril del 2021 hora: 20:13 pm
Última modificación a código
"""

from django.db import models
from django.forms import model_to_dict
from core.Usuario.models import usuario 

class empresas(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField("Nombre de la empresa",max_length=120, unique=True)
    descripcion = models.CharField("Descripción",max_length=450,blank=True)
    telefono = models.CharField("Teléfono",max_length=50, blank=True)
    nombre_contacto = models.CharField("Nombre del contacto",max_length=80,blank=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre_empresa 
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item
    
    class Meta:
        verbose_name_plural = 'empresas'
        ordering = ['id_empresa']

class departamentos(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=100, unique=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item

    class Meta:
        verbose_name_plural = "departamentos"
        ordering = ['id_departamento']

class puestos(models.Model):
    id_puesto = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(departamentos, on_delete=models.PROTECT) #protege en caso de querer borrar
    nombre = models.CharField(max_length=100)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre
    
    def toJSON(self): #función para crear diccionarios que se envían en la vista
        item = model_to_dict(self, exclude=['usuario_modificacion']) # si deseamos excluir ciertos parámetros usamos  como atributo ,exclude['']
        return item

    class Meta:
        verbose_name_plural = "puestos" #para que no le agrega una ese en el admin panel de django
        ordering = ['id_puesto']