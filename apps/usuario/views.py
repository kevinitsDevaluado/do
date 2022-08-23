import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.core.serializers import serialize

from django.utils.decorators import method_decorator
from django.views.decorators.cache import  never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView, View
from apps.usuario.models import Usuario 
from apps.usuario.mixins import SuperStaffMixin,ValidarPermisosRequeridosMixin
from .forms import FormularioLogin, FormularioUsuario, FormularioEditarUsuario, CambiarPasswordForm, FormPerfilUsuario
# Create your views here.


class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('administrador:paneladministracion')

    #Metodo decorador para poteccion de acceso 
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)
        

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


'''Para mas seguridad en los permisos de los usuarios se ha implementado 3 niveles de seguridad
   1.la Primera es que si el usuario va a loguearse
   2. La segunda va a validar si el usuario logueado es superadministrador
   3. Y la ultima es cuando el usuario ingresado posea permisos especiales de editar, eliminar'''
class InicioUsuario(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin, TemplateView):
    template_name = 'dashboard/usuarios/listarusuario.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,{'navbar':'InicioUsuario'})
    
#Clase para listar los Usuarios
class ListarUsuario(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,ListView):
    model= Usuario 
    
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True).exclude(is_superuser=True)

    '''Funcion para retornar dicinario de datos de tipo JSON'''
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            '''Forma 2 de obtener datos json a travez de serialize'''
           
            ''' Forma 1 de obtenerdatos json 
            lista_usuarios = []
            for usuario in self.get_queryset():
                data_usuario = {}
                data_usuario['id'] = usuario.id
                data_usuario['nombres'] = usuario.nombres
                data_usuario['apellidos'] = usuario.apellidos
                data_usuario['email'] = usuario.email
                data_usuario['username'] = usuario.username
                data_usuario['usuario_activo'] = usuario.usuario_activo
                lista_usuarios.append(data_usuario)#concatenar los diccionarios solicitados de data_usuario
            #Tansformar la cadena en valores json
            data = json.dumps(lista_usuarios)'''

            return HttpResponse(serialize('json',self.get_queryset()),'application/json')#Retornar esa informacionen una aplicacion Json 
        else:
            return redirect('usuarios:inicio_usuarios')

#Clase para la creacion y registro de ususarios
class RegistrarUsuario(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,CreateView):
    model = Usuario
    form_class= FormularioUsuario
    template_name = 'dashboard/usuarios/crearusuario.html'
    #Funcion para realizar la peticion AJAX
    def post(self,request, *args, **kwargs):

        if request.is_ajax():  
            form = self.form_class(data=request.POST, files = request.FILES) 
            if form.is_valid():
                nuevo_usuario = Usuario(
                    email = form.cleaned_data.get('email'),
                    username = form.cleaned_data.get('username'),
                    nombres = form.cleaned_data.get('nombres'),
                    apellidos = form.cleaned_data.get('apellidos'),
                    imagen = form.cleaned_data.get('imagen'),
                )
                nuevo_usuario.set_password(form.cleaned_data.get('password1'))
                nuevo_usuario.save()
                mensaje = f'{self.model.__name__} Registrado Correctamente!'
                error = 'No hay error '
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido Registrar el usuario!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuarios:inicio_usuarios')
    
#Clase para editar el registro de usuarios
class EditarUsuario(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,UpdateView):
    model = Usuario
    form_class = FormularioEditarUsuario
    template_name = 'dashboard/usuarios/editarusuario.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data=request.POST, files = request.FILES, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} Actualizado Correctamente!'
                error = 'No hay error '
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} No se ha podido Actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuarios:inicio_usuarios')

#Clase para eliminar usuarios
class EliminarUsuario(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,DeleteView):
    model = Usuario
    template_name = 'dashboard/usuarios/eliminarusuario.html'

    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            usuario = self.get_object()
            usuario.is_active = False
            usuario.save()
            mensaje = f'{self.model.__name__} Eliminado Correctamente!'
            error = 'No hay error '
            response = JsonResponse({'mensaje':mensaje,'error':error})
            response.status_code = 201
            return response
        else:
            return redirect('usuarios:inicio_usuarios')

class CambiarPassword(LoginRequiredMixin, View):
    template_name = 'dashboard/usuarios/cambiar_password.html'
    form_class = CambiarPasswordForm
    success_url = reverse_lazy('administrador:paneladministracion')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,{'form': self.form_class})

    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = Usuario.objects.filter(id=request.user.id)
            if user.exists():
                user = user.first()  #Obtengo el objeto
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                logout(request)
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form': form})


class EditarPerfilUsuario(LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = FormPerfilUsuario
    template_name = 'dashboard/usuarios/perfil.html'
    success_url = reverse_lazy('administrador:paneladministracion')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return self.request.user
    
    


import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

class ReporteUsuario(LoginRequiredMixin, View):
    
    def link_callback(self,uri, rel):
            
        sUrl = settings.STATIC_URL     
        
        sRoot = settings.STATIC_ROOT   
        mUrl = settings.MEDIA_URL       
        mRoot = settings.MEDIA_ROOT     

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  

        # condicion si el archivo existe
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path
                        
        
    def get(self, request,*args,**kwargs):
        try:
            template = get_template('dashboard/reportes/reporteusuario.html')
            usuario=Usuario.objects.filter(is_active=True).exclude(is_superuser=True)
            
            context = {
                'titulo': ' Reporte de registro de usuarios',
                'usuarios':usuario,
                'icon': '{}{}'.format(settings.STATIC_URL,'./assets/images/sello_white.png')
            }
            
            
            html = template.render(context)
            
            response=   HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
            
            pisaStatus = pisa.CreatePDF(
                html, dest=response,link_callback=self.link_callback
            )

            
            return response
            #return HttpResponse('hola mundo')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('administrador:inicio_usuarios'))
        
