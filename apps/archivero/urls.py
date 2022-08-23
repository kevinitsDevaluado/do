from django.urls import path
from apps.archivero.views import *

urlpatterns = [
    #redireccionamiento para listar los años del archivero
    path('inicio_anios/',Inicio_Anios.as_view(),name='inicio_anios'), 
    path('listaranios/',ListarAnios.as_view(),name='listaranios'), 
    #redireccionamiento agregar ver los años del archivero
    path('crearanios/',CrearAnios.as_view(),name='crearanios'), 
    #redireccionamiento para editar los años del archivero
    path("actualizaranios/<int:pk>/",EditarAnios.as_view(), name="actualizaranios"), 
    #redireccionamiento para eliminar los años del archivero
    path("eliminaranios/<int:pk>/",EliminarAnios.as_view(), name="eliminaranios"), 

    #redireccionamiento para listar los temas del archivero
    path('inicio_temas/',Inicio_Temas.as_view(),name='inicio_temas'), 
    path('listartemas/',ListarTemas.as_view(),name='listartemas'), 
    #redireccionamiento agregar ver los temas del archivero
    path('creartemas/',CrearTemas.as_view(),name='creartemas'), 
    #redireccionamiento para editar los temas del archivero
    path("actualizartemas/<int:pk>/",EditarTemas.as_view(), name="actualizartemas"), 
    #redireccionamiento para eliminar los temas del archivero
    path("eliminartemas/<int:pk>/",EliminarTemas.as_view(), name="eliminartemas"), 

    #redireccionamiento para listar la relacion año tema
    path('inicio_anios_temas/',Inicio_Anios_Temas.as_view(),name='inicio_anios_temas'), 
    path('listaraniostemas/',ListarAniosTemas.as_view(),name='listaraniostemas'), 
    #redireccionamiento agregar ver la relacion año tema
    path('crearaniostemas/',CrearAniosTemas.as_view(),name="crearaniostemas"), 
    #redireccionamiento para editar la relacion año tema
    path("actualizaraniostemas/<int:pk>/",EditarAniosTemas.as_view(), name="actualizaraniostemas"), 
    #redireccionamiento para eliminar la relacion año tema
    path("eliminaraniostemas/<int:pk>/",EliminarAniosTemas.as_view(), name="eliminaraniostemas"), 


    #redireccionamiento para listar documentos
    path('inicio_documentos/',Inicio_Documentos.as_view(),name='inicio_documentos'), 
    path('listardocumentos/',ListarDocumentos.as_view(),name='listardocumentos'), 
    #redireccionamiento agregar ver documentos
    path('creardocumentos/',CrearDocumentos.as_view(),name='creardocumentos'), 
    #redireccionamiento para editar documentos
    path("actualizardocumentos/<int:pk>/",EditarDocumentos.as_view(), name="actualizardocumentos"), 
    #redireccionamiento para eliminar documentos
    path("eliminardocumentos/<int:pk>/",EliminarDocumentos.as_view(), name="eliminardocumentos"), 


    path('vista_documentos/',VistaDocs.as_view(), name="vista_documentos"),

    path('lectura_documentos/',LecturaDocumentos.as_view(), name="lectura_documentos"),
    path('reporte_documentos/<int:reporte_documento>/',ReporteDocumentos.as_view(), name="reporte_documentos"),



]