"""
Software-ArtPort
Fecha: 06 de abril del 2021 hora: 20:13 pm
Última modificación a código
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Para las imagenes:
#from config.settings import MEDIA_URL,STATIC_URL

class roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=50, unique=True)
    tiene_permisos = models.CharField(max_length=2, default='No',choices=[('Si','Si'),('No','No')])
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.nombre
    
    def toJSON(self): 
        item = model_to_dict(self, exclude=['usuario_modificacion'])
        return item

    class Meta:
        verbose_name_plural = "roles"
        ordering = ['id_rol']

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombres,id_departamento,id_puesto,password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            nombres = nombres,
            id_departamento = int(id_departamento),
            id_puesto = int(id_puesto)
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,nombres,password,id_departamento,id_puesto):
        user = self.create_user(
            email,
            username = username,
            nombres = nombres,
            password = password,
            id_departamento = int(id_departamento),
            id_puesto = int(id_puesto)
        )
        user.usuario_administrador = True
        user.save()
        return user

class usuario(AbstractBaseUser):
    username = models.CharField('Usuario',max_length=20, unique=True)
    email = models.EmailField('Correo Electrónico', max_length=70,unique=True)
    nombres = models.CharField('Nombres',max_length=30,blank= True, null = True)
    apellidos = models.CharField('Apellidos',max_length=30,blank= True, null = True)
    #imagen_perfil = models.ImageField('Imagen de Perfil',upload_to='perfil/%Y/%m/%d',height_field=None, width_field=None, max_length=200,blank=True, null=True)
    #al usar imagenes instakar # pip3 install pillow
    #antes de realizar las primeras migraciones es bueno definir el modelo usurio
    #después hacemos makemigrations y migrate
    #y después creamos el superusuario
    #python3 manage.py createsuperuser
    id_departamento = models.IntegerField("Departamento",blank=True, null=True)
    id_puesto = models.IntegerField("Puesto",blank=True, null=True)
    ip_ultimo_acceso = models.CharField(max_length=50, blank=True)
    fch_ultimo_login = models.CharField(max_length=70, blank=True)
    fch_ultimo_cambio_contrasenia = models.CharField(max_length=70, blank=True)
    #fch_expiracion_contrasenia
    #crear tabla de políticas de contraseña
    #crear tabla de historial de contraseñas
    usuario_creacion = models.IntegerField(blank=True, null=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    fch_modificacion = models.DateTimeField(null=True)
    fch_cambio_password = models.DateTimeField(null=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField('Estado',max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])
    primer_ingreso = models.IntegerField(default=1,blank=True,null=True)
    cambiar_contrasenia = models.CharField(max_length=1, default='1',choices=[('1','Si'),('0','No')])
    bloqueado = models.CharField(max_length=1, default='0',choices=[('1','Bloqueado'),('0','Desbloqueado')])
    usuario_administrador = models.BooleanField(default = False)
    id_rol = models.ForeignKey(roles,on_delete=models.PROTECT,verbose_name="Perfil de Usuario",null=True)
    is_active = models.BooleanField(default=True)
    #is_staff = models.BooleanField(default = False) #esto es si puede ingresar al sitio de administración de DJANGO
    objects = UsuarioManager()
    #este campo de token se crea para la parte de reseteo de contraseña x link
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombres','id_departamento','id_puesto']

    def __str__(self):
        return self.username
    
    #para traer la ruta absoluta de imagenes usamos
    """
    def get_image(self):
        if self.imagen_perfil:
            return '{}{}'.format(MEDIA_URL, self.imagen_perfil)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    """


    #estos de abajo se borran si se usa PermisionMixin
    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador


class pantallas(models.Model):
    id_pantalla = models.AutoField(primary_key=True)
    nombre = models.CharField('Pantalla',max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "pantallas"
        ordering = ['id_pantalla']

class permisos(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(roles,on_delete=models.PROTECT,verbose_name="Perfil de Usuario")
    pantalla = models.ForeignKey(pantallas,on_delete=models.PROTECT,verbose_name="Pantalla")
    ver = models.IntegerField(default=1,blank=True,null=True)
    actualizar = models.IntegerField(default=1,blank=True,null=True)
    crear = models.IntegerField(default=1,blank=True,null=True)
    borrar = models.IntegerField(default=1,blank=True,null=True)
    fch_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.IntegerField(blank=True,null=True)
    fch_modificacion = models.CharField(max_length=35, blank=True)
    usuario_modificacion = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=1, default='1',choices=[('1','Activo'),('2','Inactivo')])
    borrado = models.CharField(max_length=1, default='0',choices=[('1','Si'),('0','No')])

    def __str__(self):
        return self.pantalla
    
    def toJSON(self): 
        item = model_to_dict(self, exclude=['usuario_modificacion'])
        return item

    class Meta:
        verbose_name_plural = "permisos"
        ordering = ['id_permiso']

