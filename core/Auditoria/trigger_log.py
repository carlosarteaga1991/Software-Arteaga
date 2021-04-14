"""
Archivo para alimentar cada acción por pantalla
se hace de esta manera ya que los Triggers varían su creación en cada base de datos
y pensando a futuro en caso que se cambie el proveedor de base de datos.
13 de abril 2021.

Por ahora ya que los log son impactados desde el ORM de django
se especifica para los tipos de acciones los siguientes:
Ingreso Exitoso
Ingreso Fallido
Usuario Bloqueado
Insertar
Modificar
Consultar
Borrar
Cerrar Sesión
Envío Correo Reseteo de Contraseña
Reseteo de Contraseña
"""

from datetime import date, datetime
from core.Auditoria.models import *
import socket #para obtener ip local


class trigger():

    def get_ip(request):
        try:
            var = request.META.get("HTTP_X_FORWARDED_FOR")
            nombre_maq = request.META.get("LOGNAME")
            if var:
                ip = var.split(",")[0]
            else:
                ip = request.META.get("REMOTE_ADDR")
        except:
            ip = ""
        return ip
    
    def get_name(request):
        try:
            nombre_maq = socket.gethostbyaddr(request.META.get("REMOTE_ADDR")) #request.META.get("REMOTE_HOST")
        except:
            nombre_maq = ""
        return nombre_maq


    def guardar(nombre_usuario, nombre_tabla,id_registro,tipo_accion,Dato_anterior,Dato_despues,campo_afectado,ip_accion,nombre_equipo):
        nuevo_log = log(
        nombre_usuario = nombre_usuario,
        nombre_tabla = nombre_tabla,
        id_registro = id_registro,
        tipo_accion = tipo_accion,
        Dato_anterior = Dato_anterior,
        Dato_despues = Dato_despues,
        campo_afectado = campo_afectado,
        ip_accion = ip_accion,
        #ip_accion = socket.gethostbyname(socket.gethostname()),
        nombre_equipo = nombre_equipo #socket.gethostname()
        )
        nuevo_log.save()
        return True

