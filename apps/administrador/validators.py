import os
from django.forms import ValidationError
from django.core.exceptions import ValidationError
#Clase para validar El peso del archivo 

class MaxSizeFileValidator:
    def __init__(self, max_file_size=5) :
        self.max_file_size = max_file_size
        
        
    def __call__(self,value):
        size = value.size
        max_size= self.max_file_size * 1048576
        if size > max_size:
            raise ValidationError(f"El tamaño maximo debe deser {self.max_file_size}MB")
        return value


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Solo se admite archivos .pdf')


    
