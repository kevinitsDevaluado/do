from django.urls import path
from apps.usuario.views import ListarUsuario, RegistrarUsuario,EditarUsuario,EliminarUsuario,InicioUsuario, CambiarPassword, EditarPerfilUsuario, ReporteUsuario

urlpatterns = [
    
    path('inicio_usuarios/',InicioUsuario.as_view(),name='inicio_usuarios'),
    path('listar_usuarios/',ListarUsuario.as_view(),name='listar_usuarios'),
    path('registrar_usuarios/',RegistrarUsuario.as_view(),name='registrar_usuarios'),
    path('editar_usuarios/<int:pk>/',EditarUsuario.as_view(),name='editar_usuarios'),
    path('eliminar_usuarios/<int:pk>/',EliminarUsuario.as_view(),name='eliminar_usuarios'),
    path('cambiar_password/', CambiarPassword.as_view(),name='cambiar_password'),
    path('perfil_usuario/', EditarPerfilUsuario.as_view(),name='perfil_usuario'),
    path('reporte_usuario/', ReporteUsuario.as_view(),name='reporte_usuario'),

    
    
    
]

