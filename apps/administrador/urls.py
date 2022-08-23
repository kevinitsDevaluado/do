from django.urls import path
from apps.administrador.views import *

urlpatterns = [

  #Pagina Principal Dashboard
  path('paneladministracion/',Paneladministracion.as_view(), name='paneladministracion'), 
    
  #redireccionamiento para ver los años de transparencia
  path('inicio_transparencia/',InicioTransparencia.as_view(), name='inicio_transparencia'),
  path('listartransparencia/',ListarTransparencia.as_view(),name='listartransparencia'),
  #redireccionamiento para agregar los años de  transparencia 
  path('creartransparencia/',CrearTransparencia.as_view(),name='creartransparencia'), 
  #redireccionamiento para editar los años de  transparencia 
  path("actualizartransparencia/<int:pk>/", ActualizarTransparencia.as_view(), name="actualizartransparencia"),
  #redireccionamiento para eliminar los años de  transparencia 
  path("eliminartransparencia/<int:pk>/", EliminarTransparencia.as_view(), name="eliminartransparencia"),


  path('inicio_mes_transparencia/',InicioMesTransparencia.as_view(), name="inicio_mes_transparencia"),
  #redireccionamiento para ver los meses que tienen transparencia
  path('listarmestransparencia/',ListarMesTransparencia.as_view(),name='listarmestransparencia'), 
  #redireccionamiento agregar ver los meses de transparencia 
  path('crearmestransparencia/',CrearMesTransparencia.as_view(),name='crearmestransparencia'), 
  #redireccionamiento para editar los meses de transparencia 
  path("editarmestransparencia/<int:pk>/", EditarMesTransparencia.as_view(), name="editarmestransparencia"),
  #redireccionamiento para eliminar los meses de  transparencia
  path("eliminarmestransparencia/<int:pk>/",EliminarMesTransparencia.as_view(), name="eliminarmestransparencia"),


  path('inicio_anio_mes_transparencia/',InicioAnioMesTransparencia.as_view(), name="inicio_anio_mes_transparencia"),
  #redireccionamiento para ver los años y meses que tiene transparencia
  path('listaraniomestransparencia/',ListarAnioMesTransparencia.as_view(),name='listaraniomestransparencia' ), 
  #redireccionamiento agregar los años y meses a transparencia
  path('crearaniomestransparencia/',CrearAnioMesTransparencia.as_view(),name='crearaniomestransparencia'), 
  #redireccionamiento para editar los años y meses a transparencia
  path('editaraniomestransparencia/<int:pk>/',EditarAnioMesTransparencia.as_view(), name="editaraniomestransparencia"),
  #redireccionamiento para eliminar los años y meses a transparencia
  path('eliminaraniomestransparencia/<int:pk>/',EliminarAnioMesTransparencia.as_view(), name="eliminaraniomestransparencia"),


  path('inicio_archivos_transparencia/',InicioArchivosTransparencia.as_view(), name="inicio_archivos_transparencia"),
  #redireccionamiento para ver los archivos que tienen transparencia
  path('listararchivostransparencia/',ListarArchivosTransparencia.as_view(),name='listararchivostransparencia' ), 
  #redireccionamiento agregar ver los archivos de transparencia
  path('creararchivostransparencia/',CrearArchivosTransparencia.as_view(),name='creararchivostransparencia'), 
  #redireccionamiento para editar los archivos de transparencia
  path("editararchivostransparencia/<int:pk>/",EditarArchivosTransparencia.as_view(), name="editararchivostransparencia"),
  #redireccionamiento para eliminar los archivos de  transparencia
  path("eliminararchivostransparencia/<int:pk>/",EliminarArchivoTransparencia.as_view(), name="eliminararchivostransparencia"),
    
    
  path('inicio_directorio/',InicioDirectorio.as_view(), name="inicio_directorio"),
  #redireccionamiento para ver directorio
  path('listardirectorio/',ListarDirectorio.as_view(),name='listardirectorio' ), 
  #redireccionamiento para agregar directorio
  path('agregardirectorio/',CrearDirectorio.as_view(),name='agregardirectorio'), 
  #redireccionamiento para editar directorio
  path("editardirectorio/<int:pk>/",EditarDirectorio.as_view(), name="editardirectorio"),
  #redireccionamiento para eliminar directorio
  path("eliminardirectorio/<int:pk>/",EliminarDirectorio.as_view(), name="eliminardirectorio"),
    
  path('inicio_asamblea/',InicioAsamblea.as_view(), name="inicio_asamblea"),
  #redireccionamiento para ver las resoluciones de asamblea
  path('listarasamblea/',ListarAsamblea.as_view(),name='listarasamblea' ), 
  #redireccionamiento para agregar resoluciones de asamblea
  path('agregarasamblea/',CrearAsamblea.as_view(),name='agregarasamblea'), 
  #redireccionamiento para editar resoluciones de asamblea
  path("editarasamblea/<int:pk>/",EditarAsamblea.as_view(), name="editarasamblea"),
  #redireccionamiento para eliminar resoluciones de asamblea
  path("eliminarasamblea/<int:pk>/",EliminarAsamblea.as_view(), name="eliminarasamblea"),
    
  path('inicio_galeria/',InicioGaleria.as_view(), name="inicio_galeria"),
  #redireccionamiento para listar los archivos que tiene la Galeria
  path('listargaleria/',ListarGaleria.as_view(),name='listargaleria'), 
  #redireccionamiento agregar ver los archivos que tiene la Galeria
  path('agregargaleria/',CrearGaleria.as_view(),name='agregargaleria'), 
  #redireccionamiento para editar los archivos que tiene la Galeria
  path("editargaleria/<int:pk>/",EditarGaleria.as_view(), name="editargaleria"), 
  #redireccionamiento para eliminar los archivos que tiene la Galeria
  path("eliminargaleria/<int:pk>/",EliminarGaleria.as_view(), name="eliminargaleria"), 



  #redireccionamiento para listar los archivos que tiene la Galeria
  path('listarprograma/',ListarPrograma.as_view(),name='listarprograma'), 
  #redireccionamiento agregar ver los archivos que tiene la Galeria
  path('agregarprograma/',CrearPrograma.as_view(),name='agregarprograma'), 
  #redireccionamiento para editar los archivos que tiene la Galeria
  path("editarprograma/<int:pk>/",EditarPrograma.as_view(), name="editarprograma"), 
  #redireccionamiento para eliminar los archivos que tiene la Galeria
  path("eliminarprograma/<int:pk>/",EliminarPrograma.as_view(), name="eliminarprograma"), 





  path('inicio_contador_vista_directorio/',Iniciocontadorvistadirectorio.as_view(),name='inicio_contador_vista_directorio'), 
  #redireccionamiento para listar el contador de directorio
  path('listarcontadorvistadirectorio/',Listarcontadorvistadirectorio.as_view(),name='listarcontadorvistadirectorio'), 
  #redireccionamiento agregar ver el contador de directorio
  path('crearcontadorvistadirectorio/',Crearcontadorvistadirectorio.as_view(),name='crearcontadorvistadirectorio'), 
  #redireccionamiento para eliminar el contador de directorio
  path("eliminarcontadorvistadirectorio/<int:pk>/",Eliminarcontadorvistadirectorio.as_view(), name="eliminarcontadorvistadirectorio"),



  path('inicio_contador_vista_asamblea/',Iniciocontadorvistaasamblea.as_view(),name='inicio_contador_vista_asamblea'), 
  #redireccionamiento para listar el contador de asamblea
  path('listarcontadorvistaasamblea/',Listarcontadorvistaasamblea.as_view(),name='listarcontadorvistaasamblea'), 
  #redireccionamiento agregar ver el contador de asamblea
  path('crearcontadorvistaasamblea/',Crearcontadorvistaasamblea.as_view(),name='crearcontadorvistaasamblea'), 
  #redireccionamiento para eliminar el contador de asamblea
  path("eliminarcontadorvistaasamblea/<int:pk>/",Eliminarcontadorvistaasamblea.as_view(), name="eliminarcontadorvistaasamblea"),



  path('Inicio_lectura_directorio/',Iniciolecturadirectorio.as_view(),name='Inicio_lectura_directorio'), 
  path('Inicio_lectura_asamblea/',Iniciolecturaasamblea.as_view(),name='Inicio_lectura_asamblea'), 
  path('Inicio_lectura_transparencia/',Iniciolecturatransparencia.as_view(),name='Inicio_lectura_transparencia'), 


  path('Reportedirectorio/<int:reporte_directorio>/',Reportedirectorio.as_view(),name='Reportedirectorio'),
  path('Reporteasamblea/<int:reporte_asamblea>/',Reporteasamblea.as_view(),name='Reporteasamblea'),
  path('Reportearchivostransparencia/<int:reporte_transparencia>/',ReporteArchivosTransparencia.as_view(),name='Reportearchivostransparencia'),
  path('Reporteprogramas/',ReporteProgramas.as_view(),name='Reporteprogramas'),
  path('Reportegaleria/',ReporteGaleria.as_view(),name='Reportegaleria'),


  #redireccionamiento para ver LA INTRODUCCION, MISION VISION AND RESENIA
  path('inicio_institucion/',InicioInstitucion.as_view(), name='inicio_institucion'),
  path('listarinstitucion/',ListarInstitucion.as_view(),name='listarinstitucion'),
  #redireccionamiento para agregar LA INTRODUCCION, MISION VISION  RESENIA
  path('crearinstitucion/',CrearInstitucion.as_view(),name='crearinstitucion'), 
  #redireccionamiento para editar LA INTRODUCCION, MISION VISION  RESENIA
  path("actualizarinstitucion/<int:pk>/", ActualizarInstitucion.as_view(), name="actualizarinstitucion"),
 
   #redireccionamiento para ver los años de transparencia
  path('inicio_preguntas/',InicioPreguntas.as_view(), name='inicio_preguntas'),
  path('listarpreguntas/',ListarPreguntas.as_view(),name='listarpreguntas'),
  #redireccionamiento para agregar los años de  transparencia 
  path('crearpreguntas/',CrearPreguntas.as_view(),name='crearpreguntas'), 
  #redireccionamiento para editar los años de  transparencia 
  path("actualizarpreguntas/<int:pk>/", ActualizarPreguntas.as_view(), name="actualizarpreguntas"),
  #redireccionamiento para eliminar los años de  transparencia 
  path("eliminarpreguntas/<int:pk>/", EliminarPreguntas.as_view(), name="eliminarpreguntas"),

  
]


