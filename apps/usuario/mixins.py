from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

class SuperStaffMixin(object):
    def dispatch(self, request, *args, **kwargs):
        '''Me valida para que al momento de acceder a la vista 
           el usuario ingresado sea superAdministrador  '''
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('administrador:paneladministracion')

class ValidarPermisosRequeridosMixin(object):
    permission_required = (
        'usuario.view_usuario',
        'usuario.add_usuario',
        'usuario.change_usuario',
        'usuario.delete_usuario',
    )
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required,str):
            return (self.permission_required)
        else:
            return self.permission_required

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('login')
        return self.url_redirect
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request,'Lo lamentamos usted no posee permisos para realizar estos cambios o acceder a estas secciones')
        return redirect(self.get_url_redirect())

