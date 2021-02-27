from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import AdminFormaCreacionUsuario, AdminFormaActualizar
from .models import Usuario
# Register your models here.


class UserAdmin(BaseUserAdmin):
    # formas para crear y actualizar instancias de usuario
    form = AdminFormaActualizar
    add_form = AdminFormaCreacionUsuario
    
    #los campos que seran utulizados para mostrar el modelo del usuario
    list_display=('correo', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields':('correo', 'password')}),
        ('Informacion personal', {'fields':('nombre', 'apellido_paterno', 'apellido_materno')}),
        ('Permisos Django', {'fields':('admin', 'staff', 'active')}),
    )
    
    add_fieldsets= (
        (None,{
            'classes':('wide',),
            'fields':('correo', 'password1', 'password2')
        }),
    )
    
    search_fields = ('correo',)
    ordering = ('correo',)
    filter_horizontal = ()
    
admin.site.register(Usuario, UserAdmin)