from django.contrib import admin
from apps.usuario.models import Usuario
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Usuario) 
admin.site.register(Permission) #muestra en el panelde administracion de Django los permisos  de cada modelo 


