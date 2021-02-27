from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


# Create your models here.
class Usuario(AbstractBaseUser):
    correo = models.EmailField(verbose_name='correo electronico', max_length=100, unique=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    
    active = models.BooleanField(_(activo), default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    
    #establecer un manejador de usuario
    objects = ManejadorUsuario()
    
    USERNAMEFIELD = 'correo' #definimos el correo como nombre de usuario
    REQUIRED_FIELDS = []#correo y contraseña son requeridos por defecto
    
    class Meta: #cambiar como aparece el nombre del modelo en la seccion de administracion de django
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        
    def get_full_name(self):
        return self.nombre+ ' ' + self.apellido_paterno + ' ' + self.apellido_materno
    
    def get_short_name(self):
        return self.nombre
    
    def has_perm(self, perm, obj=None):
        "¿El usuario cuenta con un permiso en especifico?"
        #los mas simple, si
        return True
    
    def has_module_perm(self, app_label):
        "¿El usuario cuenta con los permisos para ver una app en espefico"
        #lo mas simple, si
        
    
    @property
    def is_staff(self):
    "¿El usuario es staff (no super-usuario)?"
        return self.staff

    
    @property
    def is_admin(self):
    "El usuario es administrador (super-usuario)?"
        return self.admin
    
    @property
    def is_active(self):
    "¿El usuario esta activo?"
        return self.active
    
    def __str__(self):
        return self.nombre+ ' ' + self.apellido_paterno + ' ' + self.correo
    
    
    
    
class ManejadorUsuario(BaseUserManager):
#crea y guarda a un usuario con el correo y contraseña dadas
    def create_user(self, correo, password=None):
        if not correo:
            raise ValueError('Usuarios deben tener un correo electronico valido.')
        
        usuario = self.model(
            correo=self.normalize_email(correo),
        )
        
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
    
#crea y guarda usuario staff
    def create_staffuser(self, correo, password):
        usuario = self.create_user(
            correo,
            password=password,
        )
        usuario.staff = True
        usuario.save(using=self._db)
        return usuario
    
    
#crea y guarda un super usuario
    def create_superuser(self, correo, password):
        usuario = self.create_user(
            correo,
            password=password,            
        )
        
        usuario.staff = True
        usuario.admin = True
        usuario.save(using=self._db)
        return usuario