from django.db import models

from ckeditor.fields import RichTextField

from django.core.validators import validate_slug
# Create your models here.
from apps.administrador.models import *


class Carpeta(models.Model):
   
    nombre_car=models.PositiveIntegerField( unique=True, null=False, blank=False)
    class Meta:
        verbose_name='Carpeta'
        verbose_name_plural='Carpetas'
        db_table='carpeta'
        ordering=["id"]
    def __str__ (self):
            txt =  "Año: {0}"
            return txt.format(self.nombre_car)

    def natural_key (self):
        return self.nombre_car



class Subcarpeta(models.Model):
    MESES = (
        ('Enero','Enero'),
        ('Febrero','Febrero'),
        ('Marzo','Marzo'),
        ('Abril','Abril'),
        ('Mayo','Mayo'),
        ('Junio','Junio'),
        ('Julio','Julio'),
        ('Agosto','Agosto'),
        ('Septiembre','Septiembre'),
        ('Octubre','Octubre'),
        ('Noviembre','Noviembre'),
        ('Diciembre','Diciembre'),
    )
    
    nombre_sub=models.CharField( unique=True, max_length=200, null=False, blank=False, choices = MESES)
    class Meta:
        verbose_name='Subcarpeta'
        verbose_name_plural='Subcarpetas'
        db_table='subcarpeta'
        ordering=['-id']
    
    
    def __str__ (self):
        txt =  "Mes:{0}"
        return txt.format(self.nombre_sub) 
    
    def natural_key (self):
        return self.nombre_sub
    
    
class Carpeta_Subcarpeta(models.Model):
    fk_id_car=models.ForeignKey(Carpeta, on_delete=models.CASCADE, blank=False)
    fk_id_sub=models.ForeignKey(Subcarpeta, on_delete=models.CASCADE, blank=False)
    class Meta:
        verbose_name='Carpeta_Subcarpeta'
        verbose_name_plural='Carpetas_Subcarpetas'
        db_table='carpeta_subcarpeta'
        ordering=["id"]
        unique_together=['fk_id_car','fk_id_sub']
    def __str__ (self):
        txt =  "{0} / {1}"
        return txt.format(self.fk_id_car, self.fk_id_sub) 
    
    def natural_key(self):
        return f'{self.fk_id_car} {self.fk_id_sub}'

        
    
class Archivo(models.Model):
    fk_id_carsub=models.ForeignKey(Carpeta_Subcarpeta, on_delete=models.CASCADE)
    nombre_arch=models.CharField(max_length=100,null=False, blank=False,unique=True)
    descripcion_arch=models.CharField(max_length=100, null=False, blank=False)
    archivo_arch=models.FileField(upload_to='Archivos/%Y/%m', verbose_name='Archivo', null=False, blank=False)
    fechacreacion_arch=models.DateField('Fecha de Creacion',auto_now=False, auto_now_add = True)
    contenido_arch=models.TextField(null=True, blank=True) 
    class Meta:
        verbose_name='Archivo'
        verbose_name_plural='Archivos'
        db_table='archivo'
        ordering=["id"]
    def __str__ (self):
        txt =  "Año/Mes: {0} / archivo: {1}"
        return txt.format(self.fk_id_carsub, self.nombre_arch) 
    

    
class Directorio(models.Model):
    
    fk_id_dir=models.ForeignKey(Carpeta, on_delete=models.CASCADE)
    nombre_dir=models.CharField(max_length=100,null=False, blank=False, unique=True)
    descripcion_dir=models.CharField(max_length=100,null=False, blank=False)
    archivo_dir=models.FileField(upload_to='Directorios/%Y/%m', verbose_name='Directorio', null=False, blank=False)
    contenido_dir=models.TextField(null=True, blank=True) 
    fechacreacion_dir=models.DateField('Fecha de Creacion',auto_now=False, auto_now_add = True)
    class Meta:
        verbose_name='Directorio'
        verbose_name_plural='Directorios'
        db_table='directorio'
        ordering=["id"]
    def __str__ (self):
            txt = "{0} / Archivo: {1}"
            return txt.format(self.fk_id_dir,self.nombre_dir)
    

class Asamblea(models.Model):
    fk_id_asa=models.ForeignKey(Carpeta, on_delete=models.CASCADE)
    nombre_asa=models.CharField(max_length=100,null=False, blank=False, unique=True)
    descripcion_asa=models.CharField(max_length=100,null=False, blank=False)
    archivo_asa=models.FileField(upload_to='Asambleas/%Y/%m', verbose_name='Asamblea', null=False, blank=False)
    contenido_asa=models.TextField(null=True, blank=True) 
    fechacreacion_asa=models.DateField('Fecha de Creacion',auto_now=False, auto_now_add = True)
    class Meta:
        verbose_name='Asamblea'
        verbose_name_plural='Asambleas'
        db_table='asamblea'
        ordering=["id"]
    def __str__ (self):
        txt = "{0} / Archivo: {1}"
        return txt.format( self.fk_id_asa,self.nombre_asa)
        
    

class Galeria(models.Model):
    titulo_gal=models.CharField(max_length=100,unique=True,null=False, blank=False )
    descripcion_gal=models.CharField(max_length=100,null=False, blank=False)
    imagen_gal=models.ImageField(upload_to='Galerias/%Y/%m', verbose_name='Galeria', null=False, blank=False)
    estado_gal=models.BooleanField('Publicado/No Publicado',default=True)
    url_gal=models.URLField(max_length=100,null=True, blank=True) 
    class Meta:
        verbose_name= 'Galeria'
        verbose_name_plural= 'Galerias'
        db_table= 'galeria'
        ordering=['id']
        
    def __str__ (self):
        txt = "Imagen: {0} | {1}"
        return txt.format( self.titulo_gal, self.descripcion_gal)    
    
class Programa(models.Model):
    titulo_pro=models.CharField(max_length=100,null=False, blank=False, unique=True)
    slug = models.CharField('Slug',max_length=100,null=False, blank=False, unique=True,validators=[validate_slug])

    descripcion_pro=models.CharField(max_length=100,null=False, blank=False)
    contenido_pro=RichTextField(blank=True,null=True)

    imagen_pro=models.ImageField(upload_to='Programa/%Y/%m/', verbose_name='Programa', null=False, blank=False)

    estado_pro=models.BooleanField('Publicado/No Publicado',default=True)
    fechacreacion_pro=models.DateField('Fecha de Creacion',auto_now=False, auto_now_add = True)

    class Meta:
        verbose_name= 'Programa'
        verbose_name_plural= 'Programas'
        db_table= 'programa'
        ordering=['id']
    def __str__ (self):
        txt = "Imagen Programa: {0} | {1}"
        return txt.format( self.titulo_pro, self.descripcion_pro)   


# Creacion de modelo para contadores de visualizacion directorio

class Contadorvistasdirectorio(models.Model):
    fk_id_con=models.ForeignKey(Carpeta, on_delete=models.CASCADE, blank=False)
    directorio_con=models.IntegerField(default=0)
    estado_con=models.BooleanField('Contador/No contador',default=True)

    class Meta:
        verbose_name= 'Contadorvistasdirectorio'
        verbose_name_plural= 'Contadorvistasdirectorios'
        db_table= 'contadorvistasdirectorio'
        ordering=['id']
        unique_together=['fk_id_con']  

    def _str_ (self):
        txt = "Contador Visitas Directorio: {0}"
        return txt.format(self.directorio_con)
    
    def natural_key (self):
        return self.fk_id_con
    
    

# Creacion de modelo para contadores de visualizacion asamblea   
class Contadorvistasasamblea(models.Model):
    fk_id_cont=models.ForeignKey(Carpeta, on_delete=models.CASCADE, blank=False)
    asamblea_cont=models.IntegerField(default=0)
    estado_cont=models.BooleanField('Contador /No contador',default=True)
    class Meta:
        verbose_name='Contadorvistasasamblea'
        verbose_name_plural='Contadorvistasasambleas'
        db_table='contadorvistasasamblea'
        ordering=['id']
        unique_together=['fk_id_cont']
    def _str_(self):
        txt = "Contador Visitas Asamblea: {0}"
        return txt.format(self.asamblea_cont)
    def natural_key (self):
        return self.fk_id_cont

# Create your models here.
class Institucion(models.Model):
    introduccion = models.TextField( blank=False, null=False)
    imagen_intro = models.ImageField(upload_to='Inicio/introduccion/', verbose_name='Imagen introduccion', null=False, blank=False)
    mision= models.TextField( blank=False, null=False)
    imagen_mision = models.ImageField(upload_to='Inicio/mision/', verbose_name='Imagen Mision', null=False, blank=False)
    vision = models.TextField( blank=False, null=False)
    imagen_vision =models.ImageField(upload_to='Inicio/vision/', verbose_name='Imagen Vision', null=False, blank=False)
    resenia = models.TextField( blank=False, null=False)
    imagen_resenia =models.ImageField(upload_to='Inicio/resenia/', verbose_name='Imagen Resenia', null=False, blank=False)

    class Meta:
        verbose_name='Institucion'
        verbose_name_plural='Instituciones'
        db_table='institucion'
        ordering=["id"]


class Preguntas(models.Model):
    pregunta = models.CharField(max_length=200, blank=False, null=False)
    respuesta = models.CharField(max_length=200, blank=False, null=False)
    class Meta:
        verbose_name='Pregunta'
        verbose_name_plural='Preguntas'
        db_table='preguntas'
        ordering=["id"]
