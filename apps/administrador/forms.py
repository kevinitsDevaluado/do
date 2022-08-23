
from django import forms
from .models import *
from .validators import MaxSizeFileValidator, validate_file_extension
from django.forms import ValidationError
from ckeditor.widgets import CKEditorWidget

from datetime import date

# formulario para el modelo carpeta
class CarpetaForm(forms.ModelForm):
   
    def clean_nombre_car(self):
        today = date.today()
        nombre = self.cleaned_data['nombre_car']
        if ((nombre < today.year) or (nombre > today.year + 1)):
            raise ValidationError('Se permite la creacion del año al que se encuentra actualmente o en su caso el siguiente')
        return nombre

    class Meta:
        model = Carpeta
        fields = ['nombre_car']
        labels={
            'nombre_car':'Ingrese el año'
        }
        widgets={
            'nombre_car':forms.NumberInput  (
                attrs={
                    'class':'form-control rounded-pill',
                    'placeholder':'Ejemplo: 2022',
                    'id':'nombre_car'
                }
            )
        }


# formulario para el modelo subcarpeta
class SubcarpetaForm(forms.ModelForm):
   
    def clean_nombre_sub(self):
        nombre = self.cleaned_data["nombre_sub"]
        existe = Subcarpeta.objects.filter(nombre_sub__iexact=nombre).exists()
        if existe:
            raise ValidationError("Este nombre ya existe")
        return nombre
        
    class Meta:    
        model = Subcarpeta
        fields = ['nombre_sub']
        labels={
            'nombre_sub':'Ingrese el mes'
        }
        widgets={
            'nombre_sub':forms.Select(
                attrs={
                    'class':'form-select rounded-pill',
                    'id':'nombre_sub',
                    
                }
            )
        }




# formulario para el modelo carpeta_subcarpeta
class Carpeta_SubcarpetaForm(forms.ModelForm):
    class Meta:
        model = Carpeta_Subcarpeta
        fields = ['fk_id_car','fk_id_sub']
        labels = {
            'fk_id_car':'Seleccione el Año',
            'fk_id_sub':'Seleccione el Mes'

        }
        widgets = {
            'fk_id_car':forms.Select(
                attrs={
                    'class':'form-select rounded-pill mb-2',
                    'id':'fk_id_car'
                }
            ),
            'fk_id_sub':forms.Select(
                attrs={
                    'class':'form-select rounded-pill',
                    'id':'fk_id_sub'
                }
            )
        }
        

# formulario para el modelo archivo
class ArchivoForm(forms.ModelForm):
    archivo_arch=forms.FileField(
        validators=[
            MaxSizeFileValidator(max_file_size=2),
            validate_file_extension
        ],
        widget = forms.FileInput(
            attrs={
                    'class':'file rounded-pill mb-2',
                    'type':'file',
                    'id':'archivo_arch',
                    'accept':'application/pdf',
                    'data-preview-file-type':'text' 
                }
        )
    )

    class Meta:
        model = Archivo
        fields = ['fk_id_carsub','nombre_arch','descripcion_arch','archivo_arch','contenido_arch']
        labels = {
            'fk_id_carsub':'Año y mes a que Corresponde:',
            'nombre_arch': 'Titulo del Archivo',
            'descripcion_arch': 'Breve descripcion del archivo',
            'archivo_arch':  'Seleccione un Archivo en Formato PDF',
            'contenido_arch': 'Realizar Lectura',

        }
        widgets = {
            'fk_id_carsub': forms.Select(
                attrs={
                    'class':'form-select rounded-pill',
                    'id':'fk_id_carsub'
                }
            ),

            'nombre_arch': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill',
                    'placeholder':'Ingrese el titulo del archivo',
                    'id':'nombre_arch'
                }
            ),

            'descripcion_arch': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill',
                    'placeholder':'Ingrese una breve descripcion del archivo',
                    'id':'descripcion_arch'
                }
            ),
            'contenido_arch':forms.CheckboxInput(
                attrs={
                    'class':'form-check-input mt-2 mb-2',
                    'type':'checkbox',
                }
            )
          
        }
        
# formulario para el modelo archivo
class ActualizarArchivoForm(forms.ModelForm):
    archivo_arch=forms.FileField(
        validators=[
            MaxSizeFileValidator(max_file_size=2),
            validate_file_extension
        ],
        widget = forms.FileInput(
            attrs={
                    'class':'file rounded-pill mb-2',
                    'type':'file',
                    'id':'archivo_arch',
                    'accept':'application/pdf',
                    'data-preview-file-type':'text' 
                }
        )
    )

    class Meta:
        model = Archivo
        fields = ['fk_id_carsub','nombre_arch','descripcion_arch','archivo_arch']
        labels = {
            'fk_id_carsub':'Año y mes a que Corresponde:',
            'nombre_arch': 'Titulo del Archivo',
            'descripcion_arch': 'Breve descripcion del archivo',
            'archivo_arch':  'Seleccione un Archivo en Formato PDF',

        }
        widgets = {
            'fk_id_carsub': forms.Select(
                attrs={
                    'class':'form-select rounded-pill',
                    'id':'fk_id_carsub'
                }
            ),

            'nombre_arch': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill',
                    'placeholder':'Ingrese el titulo del archivo',
                    'id':'nombre_arch'
                }
            ),

            'descripcion_arch': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill',
                    'placeholder':'Ingrese una breve descripcion del archivo',
                    'id':'descripcion_arch'
                }
            ),
          
        }
        

        
# formulario para el moodelo directorio
class ResolucionesdedirectorioForm(forms.ModelForm):
    archivo_dir=forms.FileField(
        validators=[
            MaxSizeFileValidator(max_file_size=2),
            validate_file_extension
        ],
        widget = forms.FileInput(
            attrs={
                    'class':'file form-control rounded-pill mb-2',
                    'type':'file',
                    'id':'archivo_dir',
                    'accept':'application/pdf',
                    'data-preview-file-type':'text' 
                }
        ),
        label='Seleccione un Archivo en Formato PDF'
    )
    class Meta:
        model = Directorio
        fields = ['fk_id_dir','nombre_dir','descripcion_dir','archivo_dir','contenido_dir']

        labels = {
            'fk_id_dir':'Año a que Corresponde:',
            'nombre_dir': 'Titulo del Archivo',
            'descripcion_dir': 'Breve descripcion del archivo',
            'contenido_dir': 'Realizar Lectura Si/No:',
        }
        widgets = {
            'fk_id_dir': forms.Select(
                attrs={
                    'class':'form-select rounded-pill mb-2',
                    'id':'fk_id_dir'
                }
            ),

            'nombre_dir': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese el titulo del archivo',
                    'id':'nombre_dir'
                }
            ),

            'descripcion_dir': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese una breve descripcion del archivo',
                    'id':'descripcion_dir'
                }
            ),
            'contenido_dir':forms.CheckboxInput(
                attrs={
                    'class':'form-check-input mt-2 mb-2',
                    'type':'checkbox'
                }
            )

        }

class EditarResolucionesdedirectorioForm(forms.ModelForm):
    archivo_dir=forms.FileField(
        validators=[
            MaxSizeFileValidator(max_file_size=2),
            validate_file_extension
        ],
        widget = forms.FileInput(
            attrs={
                    'class':'file form-control rounded-pill mb-2',
                    'type':'file',
                    'id':'archivo_dir',
                    'accept':'application/pdf',
                    'data-preview-file-type':'text' 
                }
        ),
        label='Seleccione un Archivo en Formato PDF'
    )
    class Meta:
        model = Directorio
        fields = ['fk_id_dir','nombre_dir','descripcion_dir','archivo_dir']

        labels = {
            'fk_id_dir':'Año a que Corresponde:',
            'nombre_dir': 'Titulo del Archivo',
            'descripcion_dir': 'Breve descripcion del archivo',
            'contenido_dir': 'No leer/Leer',
        }
        widgets = {
            'fk_id_dir': forms.Select(
                attrs={
                    'class':'form-select rounded-pill mb-2',
                    'id':'fk_id_dir'
                }
            ),

            'nombre_dir': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese el titulo del archivo',
                    'id':'nombre_dir'
                }
            ),

            'descripcion_dir': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese una breve descripcion del archivo',
                    'id':'descripcion_dir'
                }
            ),
        }
        
        
# formulario para el modelo asamblea
class AsambleaForm(forms.ModelForm):
    archivo_asa=forms.FileField(
        validators=[
            MaxSizeFileValidator(max_file_size=2),
            validate_file_extension
        ],
        widget = forms.FileInput(
            attrs={
                'class':'file form-control rounded-pill mb-2',
                'type':'file',
                'id':'archivo_asa',
                'accept':'application/pdf',
                'data-preview-file-type':'text' 
            }
        ),
        label='Seleccione un Archivo en Formato PDF'
    )
    class Meta:
        model = Asamblea
        fields = ['fk_id_asa','nombre_asa','descripcion_asa','archivo_asa','contenido_asa']

        labels = {
            'fk_id_asa':'Año a que Corresponde:',
            'nombre_asa': 'Titulo del Archivo',
            'descripcion_asa': 'Breve descripcion del archivo',
            'contenido_asa': 'Realizar Lectura Si/No',
        }

        widgets = {
            'fk_id_asa': forms.Select(
                attrs={
                    'class':'form-select rounded-pill mb-2',
                    'id':'fk_id_asa',
                }
            ),

            'nombre_asa': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese el titulo del archivo',
                    'id':'nombre_asa',
                }
            ),

            'descripcion_asa': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese una breve descripcion del archivo',
                    'id':'descripcion_asa'
                }
            ),
            'contenido_asa':forms.CheckboxInput(
                attrs={
                    'class':'form-check-input mt-2 mb-2',
                    'type':'checkbox'
                }
            )
        }



# formulario para el modelo asamblea
class EditarAsambleaForm(forms.ModelForm):
    archivo_asa=forms.FileField(
        validators=[
            MaxSizeFileValidator(max_file_size=2),
            validate_file_extension
        ],
        widget = forms.FileInput(
            attrs={
                'class':'file form-control rounded-pill mb-2',
                'type':'file',
                'id':'archivo_asa',
                'accept':'application/pdf',
                'data-preview-file-type':'text' 
            }
        ),
        label='Seleccione un Archivo en Formato PDF'
    )
    class Meta:
        model = Asamblea
        fields = ['fk_id_asa','nombre_asa','descripcion_asa','archivo_asa']

        labels = {
            'fk_id_asa':'Año a que Corresponde:',
            'nombre_asa': 'Titulo del Archivo',
            'descripcion_asa': 'Breve descripcion del archivo',
        }

        widgets = {
            'fk_id_asa': forms.Select(
                attrs={
                    'class':'form-select rounded-pill mb-2',
                    'id':'fk_id_asa',
                }
            ),

            'nombre_asa': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese el titulo del archivo',
                    'id':'nombre_asa',
                }
            ),

            'descripcion_asa': forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese una breve descripcion del archivo',
                    'id':'descripcion_asa'
                }
            ),
        }




# formulario para el modelo galeria
class Galeriaform(forms.ModelForm):
    imagen_gal=forms.FileField(
        label="Carge una imagen",
        validators=[MaxSizeFileValidator(max_file_size=2)],
        widget = forms.FileInput(
            attrs={
                'class':'file form-control rounded-pill mb-2',
                'type':'file',
                'id':'imagen_gal',
                'accept':'image/*',
                'data-preview-file-type':'text'  
            }  
        ),   
    )
    
    class Meta:
        model = Galeria
        fields = ['titulo_gal','descripcion_gal','imagen_gal','url_gal','estado_gal']
        labels = {
            'titulo_gal':'Titulo de la Imagen',
            'descripcion_gal':'Breve Descripcion de la imagen',
            'estado_gal':'Publicado / No Publicado',
            'url_gal':'Ingrese un enlace ¡Recuerde que no es necesario este campo!'
        }
        widgets = {
            'titulo_gal':forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Ingrese el titulo de la imagen',
                    'id':'titulo_gal',
                }
            ),

            'descripcion_gal':forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill mb-2',
                    'placeholder':'Describa el contenido de la Imagen',
                    'id':'descripcion_gal'
                }
            ),
            'estado_gal':forms.CheckboxInput(
                attrs={
                    'class':'form-check-input  mb-2 mt-2',
                    'type':'checkbox',
                    'id':'estado_gal'
                }
            ),
            'url_gal':forms.URLInput( 
                attrs={
                    'class':'form-control mb-2 mt-2 rounded-pill',
                    'type':'url',
                    'placeholder':'https://ejemplo.com/users/',
                    'aria-describedby':'basic-addon3',
                    'id':'url_gal'
                }
            )

        }
    
   

# formulario para el modelo Programa 
class Programaform(forms.ModelForm):
    imagen_pro=forms.FileField(
        label="Suba una imagen",
        validators=[MaxSizeFileValidator(max_file_size=2)],
        widget = forms.FileInput(
            
            attrs={
                    'class':'file form-control rounded-pill mb-2',
                    'type':'file',
                    'id':'formFile',
                    'accept':'image/*',
                    'data-preview-file-type':'text'  
            }
            
        ),   
    )

    contenido_pro = forms.CharField(
        label="Escriba el contenido que tendra",
        widget=CKEditorWidget()
    )

   
    class Meta:
        model = Programa
        fields = ['titulo_pro','descripcion_pro','slug','contenido_pro','imagen_pro','estado_pro']
        labels = {
            'titulo_pro':'Titulo del Programa',
            'slug':'Nombre de la  Direccion o SLUG',
            'descripcion_pro':'Breve Descripcion del Programa',
            'estado_pro':'Publicado / No Publicado'     
        }
        widgets = {
            'titulo_pro':forms.TextInput(
                attrs={
                    'class':'form-control mb-2 rounded-pill',
                    'placeholder':'Ingrese el titulo de la imagen'
                }
            ),

            'descripcion_pro':forms.TextInput(
                attrs={
                    'class':'form-control mb-2 rounded-pill',
                    'placeholder':'Describa el contenido de la Imagen'
                }
            ),
            'slug':forms.TextInput(
                attrs={
                    'class':'form-control mb-2 rounded-pill',
                    'placeholder':'Ejemplo: Actividad1'
                }
            ),
            'estado_pro':forms.CheckboxInput(
                attrs={
                    'class':'form-check-input mt-2 mb-2',
                    'type':'checkbox'
                }
            )

        }

 
# formulario para el modelo Contador visualizacion para la seccion resolucion de directorio
class ContadorvistasdirectorioForm(forms.ModelForm):
    class Meta:
        model = Contadorvistasdirectorio
        fields = ['fk_id_con','directorio_con']
        labels = {
            'fk_id_con':'Seleccione el año a crear un contador',
            'directorio_con':'El contador por defecto se va a posicionar en 0'
        }
        widgets = {
            'fk_id_con':forms.Select(
                attrs={
                    'class':'form-select rounded-pill mb-2'
                }  
            ),

            'directorio_con':forms.HiddenInput(
                attrs={
                    'class':'form-control',
                    'type':'hidden',

                }
            )
        }
        
        
        
# formulario para el modelo Contador visualizacion para la seccion resolucion de directorio
class ContadorvistasasambleaForm(forms.ModelForm):
    class Meta:
        model = Contadorvistasasamblea
        fields = ['fk_id_cont','asamblea_cont']
        labels = {
            'fk_id_cont':'Seleccione el año a crear un contador',
            'asamblea_cont':'El contador por defecto se va a posicionar en 0'
        }
        widgets = {
            'fk_id_cont':forms.Select(
                attrs={
                    'class':'form-select rounded-pill mb-2'
                }  
            ),

            'asamblea_cont':forms.HiddenInput(
                attrs={
                    'class':'form-control',
                    'type':'hidden',

                }
            )
        }


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = [
            'introduccion','imagen_intro',
            'mision','imagen_mision',
            'vision','imagen_vision',
            'resenia','imagen_resenia'
        ]
        labels ={
            'introduccion':'Ingrese contenido para la Introducción',
            'imagen_intro':'Suba una imagen referente a la Introduccion',
            'mision':'Ingrese la mision de la Asociación',
            'imagen_mision':'Suba una imagen referente a la Misión',
            'vision':'Ingrese la vision de la Asociación',
            'imagen_vision':'Suba una imagen referente a la Misión',
            'resenia':'Ingrese la Reseña Historica de la Asociación',
            'imagen_resenia':'Suba una imagen referente a la Reseña Historica'
        }
        widgets={
            'introduccion':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'id':'introduccion',
                }
            ),
            'imagen_intro':forms.FileInput(
                attrs={
                    'class':'form-control mb-4',
                    'id':'imagen_intro',
                 
                }
            ),
            'mision':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'id':'mision',
                }
            ),
            'imagen_mision':forms.FileInput(
                attrs={
                    'class':'form-control mb-4',
                    'id':'imagen_vision',
                }
            ),
            'vision':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'id':'vision',
                }
            ),
            'imagen_vision':forms.FileInput(
                attrs={
                    'class':'form-control mb-4',
                    'id':'imagen_vision',
                }
            ),
            'resenia':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'id':'resenia',
                }
            ),
            'imagen_resenia':forms.FileInput(
                attrs={
                    'class':'form-control mb-2',
                    'id':'imagen_resenia',
                }
            ),
        }

class PreguntasForm(forms.ModelForm):
    class Meta:
        model = Preguntas
        fields = ['pregunta','respuesta']
        labels ={
            'pregunta':'Ingrese una pregunta',
            'respuesta':'Escriba la respuesta a la pregunta',
        }
        widgets={
            'pregunta':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'pregunta',
                }
            ),
            'respuesta':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'respuesta',
                }
            ),
            
        }
