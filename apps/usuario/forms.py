from django import forms
from apps.usuario.models import Usuario
from django.contrib.auth.forms import AuthenticationForm

#Formulario para el login del sistema
class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

#Forulario para crud de usuario 
class FormularioUsuario(forms.ModelForm):
    '''Formulario de registro de Usuario en la base de datos
       variables:
        -password1: Contraseña
        -password2: Verificación de la contraseña
    '''
    password1 = forms.CharField(
        label='Contraseña',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Ingrese su Contraseña...',
                'id':'password1',
                'required':'required',
                'type':'password',
            }
        )
    )

    password2 = forms.CharField(
        label = 'Confirmar Contraseña',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Ingrese nuevamente su Contraseña...',
                'id':'password2',
                'required':'required',
                'type':'password',
            }
        )  
    )

    class Meta:
        model = Usuario
        fields = ('email','username','nombres','apellidos','imagen')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese su correo electrónico.....',
                    'type':'email',
                    'id':'email'
                }
            ),
            'username':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ejemplo: JuanPere10....',
                    'id':'username',
                }
            ),
            'nombres':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese sus nombres....',
                    'id':'nombres'
                }
            ),
            'apellidos':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese sus apellidos....',
                    'id':'apellidos'
                }
            ), 
        }
    
    def __init__(self, *args, **kwargs):
        super(FormularioUsuario, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({
            'class': 'form-control rounded-pill', 
        })
    
    '''
        Metodo para validar que ambas contraseñas sean iguales antes de ser encriptadas
        y guardadas en la base de datos y asi retornar la contraseña valid

        Excepciones: 
            -validationError: mensaje que se va a utilizar para el usuario especificando 
            que las contraseñas no son iguales
    '''
    def clean_password2(self):
        password1=self.cleaned_data.get('password1') #extraer lo que hay en passwor1
        password2=self.cleaned_data.get('password2') #extraer lo que hay en passwor2  

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2 #Se retorna para no impedir el flujo y el proceso de validacion 

    '''Metodo para redefinir el campo de pasword'''
    def save(self, commit=True):  #commit sirve para que proceda con el registro
        user = super().save(commit=False) #cuande se cambia a false se guarda la instancia o la informacion que se pretende guardar en algn momento del ciclo 
        user.set_password(self.cleaned_data['password1']) #Metodo que encripta las contraseñas y con cleaned_data le hacemos que encripte la cotraseña 
        if commit:
            user.save()
        return user 


#Formulario para edicion de usuario y asi pueda que las contraseñas no se modifiuen

class FormularioEditarUsuario(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('email','username','nombres','apellidos','imagen')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese su correo electrónico.....',
                    'type':'email',
                    'id': 'email',
                }
            ),
            'username':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ejemplo: JuanPere10....',
                    'id':'username',
                }
            ),
            'nombres':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese sus nombres....',
                    'id':'nombres',
                }
            ),
            'apellidos':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese sus apellidos....',
                    'id':'apellidos'
                }
            ),    
        }

    def __init__(self, *args, **kwargs):
        super(FormularioEditarUsuario, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({
            'class': 'form-control rounded-pill', 
        })
    
    def save(self, commit=True):  #commit sirve para que proceda con el registro
        user = super().save(commit=False) #cuande se cambia a false se guarda la instancia o la informacion que se pretende guardar en algn momento del ciclo 
        if commit:
            user.save()
        return user 
 


class CambiarPasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Contraseña',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Ingrese su Nueva Contraseña...',
                'id':'password1',
                'required':'required',
                'type':'password',
            }
        )
    )

    password2 = forms.CharField(
        label = 'Confirmar Contraseña',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Ingrese denuevo su Nueva Contraseña...',
                'id':'password2',
                'required':'required',
                'type':'password',
            }
        )  
    )

    def clean_password2(self):
        password1=self.cleaned_data.get('password1') #extraer lo que hay en passwor1
        password2=self.cleaned_data.get('password2') #extraer lo que hay en passwor2  

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2 #Se retorna para no impedir el flujo y el proceso de validacion 




class FormPerfilUsuario(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('email','username','nombres','apellidos','imagen')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese su correo electrónico.....',
                    'type':'email',
                    'id': 'email',
                }
            ),
            'username':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ejemplo: JuanPere10....',
                    'id':'username',
                }
            ),
            'nombres':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese sus nombres....',
                    'id':'nombres',
                }
            ),
            'apellidos':forms.TextInput(
                attrs={
                    'class': 'form-control rounded-pill',
                    'placeholder': 'Ingrese sus apellidos....',
                    'id':'apellidos'
                }
            ),    
        }

    def __init__(self, *args, **kwargs):
        super(FormPerfilUsuario, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({
            'class': 'form-control rounded-pill', 
            'id':'imagen'
        })
    
    def save(self, commit=True):  #commit sirve para que proceda con el registro
        user = super().save(commit=False) #cuande se cambia a false se guarda la instancia o la informacion que se pretende guardar en algn momento del ciclo 
        if commit:
            user.save()
        return user 
 


