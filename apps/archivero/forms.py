from django import forms
from .models import *
from apps.administrador.validators import MaxSizeFileValidator, validate_file_extension
from django.forms import ValidationError
from datetime import date

# formulario para el modelo carpeta
class AnioForm(forms.ModelForm):

    def clean_nombre_ani(self):
        today = date.today()
        nombre = self.cleaned_data['nombre_ani']
        if ((nombre < today.year - 10) or (nombre > today.year + 1)):
            raise ValidationError(f'Se permite la creacion del año al que se encuentra actualmente {today.year} desde {today.year - 10} o en su caso hasta {today.year +   1} ')
        return nombre
   
    class Meta:
        model = Anios
        fields = ['nombre_ani']
        labels={
            'nombre_ani':'Ingrese el año'
        }
        widgets={
            'nombre_ani':forms.NumberInput  (
                attrs={
                    'class':'form-control rounded-pill',
                    'placeholder':'Ejemplo: 2022',
                    'id':'nombre_ani'
                }
            )
        }


# formulario para el modelo subcarpeta
class TemasForm(forms.ModelForm):
   
    def clean_nombre_tem(self):
        nombre = self.cleaned_data["nombre_tem"]
        existe = Temas.objects.filter(nombre_tem__iexact=nombre).exists()
        if existe:
            raise ValidationError("Este nombre ya existe")
        return nombre
        
    class Meta:    
        model = Temas
        fields = ['nombre_tem']
        labels={
            'nombre_tem':'Ingrese el TEMA de la Subcarpeta'
        }
        widgets={
            'nombre_tem':forms.TextInput(
                attrs={
                    'class':'form-control rounded-pill',
                    'placeholder':'Ejemplo: CONVENIOS',
                    'id':'nombre_tem'
                }
            )
        }




# formulario para el modelo carpeta_subcarpeta
class Anio_TemasForm(forms.ModelForm):
    class Meta:
        model = Anios_Temas
        fields = ['fk_id_ani','fk_id_tem']
        labels = {
            'fk_id_ani':'Seleccione el Año',
            'fk_id_tem':'Seleccione el Tema'

        }
        widgets = {
            'fk_id_ani':forms.Select(
                attrs={
                    'class':'form-select rounded-pill mb-2',
                    'id':'fk_id_ani',
                }
            ),
            'fk_id_tem':forms.Select(
                attrs={
                    'class':'form-select rounded-pill',
                    'id':'fk_id_tem',
                }
            )
        }
        

# formulario para el modelo archivo
class DocumentosForm(forms.ModelForm):
    documento_doc=forms.FileField(
        validators=[
            MaxSizeFileValidator(max_file_size=2),
            validate_file_extension
        ],
        widget = forms.ClearableFileInput(
            attrs={
                    'class':'file form-control rounded-pill mb-2',
                    'type':'file',
                    'id':'documento_doc',
                    'accept':'application/pdf',
                    'data-preview-file-type':'text' 
                }
        )
    )

    class Meta:
        model = Documentos
        fields = ['fk_id_atem','documento_doc','contenido_doc']
        labels = {
            'fk_id_atem':'Año y Tema a que Corresponde:',
            'documento_doc':'Seleccione un Docuemnto en Formato PDF',
            'contenido_doc': 'Realizar lectura Si/No',
        }
        widgets = {
            'fk_id_atem': forms.Select(
                attrs={
                    'class':'form-select rounded-pill',
                    'id':'fk_id_atem',
                }
            ),
            
            'contenido_doc':forms.CheckboxInput(
                attrs={
                    'class':'form-check-input mt-2 mb-2',
                    'type':'checkbox'
                    
                }
            )
        }
        


# formulario para el modelo archivo
class EditarDocumentosForm(forms.ModelForm):
    documento_doc=forms.FileField(
        validators=[
            MaxSizeFileValidator(max_file_size=2),
            validate_file_extension
        ],
        widget = forms.ClearableFileInput(
            attrs={
                    'class':'file form-control rounded-pill mb-2',
                    'type':'file',
                    'id':'documento_doc',
                    'accept':'application/pdf',
                    'data-preview-file-type':'text' 
                }
        )
    )

    class Meta:
        model = Documentos
        fields = ['fk_id_atem','documento_doc']
        labels = {
            'fk_id_atem':'Año y Tema a que Corresponde:',
            'documento_doc':'Seleccione un Docuemnto en Formato PDF',
        }
        widgets = {
            'fk_id_atem': forms.Select(
                attrs={
                    'class':'form-select rounded-pill',
                    'id':'fk_id_atem',
                }
            ),
        }
        
