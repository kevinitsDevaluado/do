from django.contrib import admin
from apps.administrador.models import *


# Register your models here.

admin.site.register(Carpeta) 
admin.site.register(Subcarpeta) 
admin.site.register(Archivo) 
admin.site.register(Carpeta_Subcarpeta) 
admin.site.register(Directorio) 
admin.site.register(Asamblea) 
admin.site.register(Galeria)
admin.site.register(Programa)
admin.site.register(Contadorvistasdirectorio)
admin.site.register(Contadorvistasasamblea)
admin.site.register(Institucion)
admin.site.register(Preguntas)
