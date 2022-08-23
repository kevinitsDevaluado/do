from django.db import models
from django.core.validators import  MinLengthValidator

# Create your models here.
class Anios(models.Model):
   
    nombre_ani=models.PositiveIntegerField( unique=True, null=False, blank=False)
    class Meta:
        verbose_name='Anio'
        verbose_name_plural='Anios'
        db_table='anio'
        ordering=["id"]
    def __str__ (self):
            txt =  "Año: {0}"
            return txt.format(self.nombre_ani)

    def natural_key (self):
        return self.nombre_ani



class Temas(models.Model):
    nombre_tem=models.CharField(max_length=100,validators=[MinLengthValidator(4)], unique=True, null=False, blank=False)
    class Meta:
        verbose_name='Tema'
        verbose_name_plural='Temas'
        db_table='temas'
        ordering=['id']
    
    
    def __str__ (self):
        txt =  "Tema:{0}"
        return txt.format(self.nombre_tem) 
    
    def natural_key (self):
        return self.nombre_tem
    
    
class Anios_Temas(models.Model):
    fk_id_ani=models.ForeignKey(Anios, on_delete=models.CASCADE, blank=False)
    fk_id_tem=models.ForeignKey(Temas, on_delete=models.CASCADE, blank=False)
    class Meta:
        verbose_name='Anio_Tema'
        verbose_name_plural='Anios_Temas'
        db_table='anio_tema'
        ordering=["id"]
        unique_together=['fk_id_ani','fk_id_tem']
    def __str__ (self):
        txt =  "{0} / {1}"
        return txt.format(self.fk_id_ani, self.fk_id_tem) 
    
    def natural_key(self):
        return f'{self.fk_id_ani} {self.fk_id_tem}'

        
    
class Documentos(models.Model):
    fk_id_atem=models.ForeignKey(Anios_Temas, on_delete=models.CASCADE)
    documento_doc=models.FileField(upload_to='Archivero/%Y/%m', verbose_name='Documento', null=False, blank=False)
    fechacreacion_doc=models.DateField('Fecha de Creacion',auto_now=False, auto_now_add = True)
    contenido_doc=models.TextField(null=True, blank=True) 

    class Meta:
        verbose_name='Documento'
        verbose_name_plural='Documentos'
        db_table='documento'
        ordering=["id"]
    def __str__ (self):
        txt =  "Año/Tema: {0}, Documento: {1} "
        return txt.format(self.fk_id_atem, self.documento_doc) 
    
