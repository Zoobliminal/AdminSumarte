#URLS APP LOGIN

from django.urls import path
from .views import vistaRegistro, cerrar_sesion, loguear

urlpatterns = [
    
    path('', vistaRegistro.as_view(), name="registro"),
    path('login', loguear, name="login"),
    path('cerrar_sesion', cerrar_sesion, name="cerrar_sesion"),
]
