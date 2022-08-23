from django.urls import path

from apps.publico.views import  Contadorvistaasambleas, Contadorvistadirectorios, Resoluciones, Transparencia, Verasamblea, Verdirectorio


from .views import *

urlpatterns =[
    path('',Home.as_view(), name='index'),
    path('nosotros/',nosotros, name='nosotros'),
    path('programas/',programas,name='programas'),
    
    # redirigiendo a transparencia
    path('transparencia/',Transparencia.as_view(),name='transparencia'), 
    
    # redirigiendo resoluciones
    path('resoluciones/',Resoluciones.as_view(),name='resoluciones'), 


     #ver directorio
    path('resolucionesdedirectorio/<int:directorio_id>/',Verdirectorio.as_view(),name='resolucionesdedirectorio'), 

    
    # redirigiendo resoluciones de direccion ejecutiva 
    path("resolucionesdeasamblea/<int:asamblea_id>/", Verasamblea.as_view(),name="resolucionesdeasamblea" ),




    # redirigiendo ver cantidad de  visualizacion de directorio
   path('resolucionesdedirectorio/verdescargar/<int:vista_id>/', Contadorvistadirectorios.as_view(), name='verdescargar'),
  

    
    # redirigiendo ver cantidad de  visualizacion de asamblea
    path('resolucionesdeasamblea/vistaasamblea/<int:vistaasamblea_id>/', Contadorvistaasambleas.as_view(), name='vistaasamblea'),



]