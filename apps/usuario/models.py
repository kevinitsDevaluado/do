
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
#definiendo mi modelo de Usuario pero primero pasa por el usuario manager que es definido por django

class UsuarioManager(BaseUserManager):
    #Funcion para crear usuarios y va a ser utilizada cuando se use la terminal
    def _create_user(self, username, email, nombres,password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            nombres = nombres,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
        
    def create_user(self,username,email,nombres,password=None, **extra_fields):
        return self._create_user(username,email,nombres,password,False,False,**extra_fields)  

    def create_superuser(self,username,email,nombres,password=None,**extra_fields):
        return self._create_user(username,email,nombres,password,True,True,**extra_fields)

#Definiendo el modelo del usuario personalizado
'''En la creacion de usuarios debe de tener perminos que van a heredar de permision MIXIN
   Y este va a heredar de PermissionsMixin y va despues de AbstractBaseUserpor la jerarquia
   que corresponde'''
class Usuario(AbstractBaseUser,PermissionsMixin):
    username = models.CharField('Nombre de Usuario', unique=True, max_length=100)
    email = models.EmailField('Correo Electronico', max_length=255, unique=True)
    nombres = models.CharField('Nombres',max_length=200,blank=True, null=True)
    apellidos = models.CharField('Apellidos',max_length=200, blank=True, null=True)
    imagen = models.ImageField('Imagen de perfil', upload_to='perfil/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects= UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS= ['email', 'nombres','apellidos']

    def __str__(self):
        return f'{self.nombres},{self.apellidos}'

    
    
    


    
