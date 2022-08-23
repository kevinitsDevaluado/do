"""asociacionutc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.administrador.views import *
from apps.publico.views import *

from django.urls.conf import re_path

from django.conf import settings
from django.views.static import serve
from apps.usuario.views import Login, logoutUsuario
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),


    #Rediiguien ala vistra peincipal
    path('',include(('apps.publico.urls','publico'))),

    path('archivero/',include(('apps.archivero.urls','archivero'))),


    #redireccionamiento de urls de la aplicacion usuarios
    path('usuarios/',include(('apps.usuario.urls','usuarios'))),

    #redireccionamiento de urls de la aplicacion administrador
    path('indexadmin/',include(('apps.administrador.urls','administrador'))),

   
  
   


    #Redireccionamiento del acceso al login
    path('accounts/login/',Login.as_view(),name='login'),

    #Redireccionamiento para salir delogin 
    path('logout/', login_required( logoutUsuario),name='logout'),

    path('<slug:slug>/',detalleprograma, name='detalleprograma'),

]




urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
  

]
