from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Usuario

#crear usuario en consolo
class FormaRegistro(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget= forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ('correo',)
        
    def clean_email(self):
        correo = self.cleaned_data.get('correo')
        qs = Usuario.objects.filter(correo = correo)
        if qs.exists():
            raise forms.ValidationError("correo ya registrado")
        return correo
    
    def clean_password2(self):
        # revisar que las contraseñas coincidan
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Contraseñas no coinciden")
        return password2

#forma para crear nuevos usuarios. incluyen todos los campos requeridos
class AdminFormaCreacionUsuario(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget= forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ('correo', 'nombre', 'apellido_paterno', 'apellido_materno')
        
    def clean_password2(self):
        # revisar que las contraseñas coincidan
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Contraseñas no coinciden")
        return password2
    
    def save(self, commit=True):
        #guardar contraseña en formato hash
        usuario = super(AdminFormaCreacionUsuario, self).save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        
        if commit:
            usuario.save()
        return usuario
        
        
#forma para actualizar un usuario. incluye todos los campos requeridos, pero remplaza el campo de contraseña
#con el Hash guardado en el admin de django
class AdminFormaActualizar(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = Usuario
        fields = ('correo', 'nombre', 'apellido_paterno', 'apellido_materno', 'active', 'admin')
        
    def clean_password(self):
        #regresa el valor inicial, sin importar lo que el usuario escriba
        #se realiza ya que el campo no tiene acceso al valor inicial,
        #las contraseñas en django requieren un formato en especifico
        return self.initial['password']
    