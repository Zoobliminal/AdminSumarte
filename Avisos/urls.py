#URLS APP AVISOS

from django.urls import path
from . import views
from .views import EditarAvisoView


urlpatterns = [
    path('', views.avisos, name="avisos"),
    path('cargar_datos_iniciales/', views.cargar_datos_iniciales, name='cargar_datos_iniciales'),
    path('avisos/', views.avisos, name="avisos"),
    path('aviso_nuevo/', views.aviso_nuevo, name="aviso_nuevo"),
    path('avisos_cerrados/', views.avisos_cerrados, name="avisos_cerrados"),
    path('aviso/editar/<int:pk>/', EditarAvisoView.as_view(), name='editar_aviso'),
    path('aviso_detalle/<int:aviso_id>/', views.aviso_detalle, name='aviso_detalle'),
    path('reabrir_aviso/<int:aviso_id>/', views.reabrir_aviso, name='reabrir_aviso'),
    path('insertar_comentario/<int:aviso_id>/', views.agregarImageComentAviso, name='insertarComentario'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('asignar_trabajador/<int:aviso_id>/', views.asignar_trabajador, name='asignar_trabajador'),
    path('eliminar_asignacion/<int:trabajador_id>', views.eliminar_asignacion, name='eliminar_asignacion'),
    path('cambiar_estado/<int:aviso_id>/', views.cambiar_estado, name='cambiar_estado'),
   
]

