#URLS APP INSTALACIONES

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.instalaciones, name='instalaciones'),
    path('mapa/', views.mapa_instalaciones, name='mapa_instalaciones'),
    path('instalacion/<int:instalacion_id>/', views.detalle_instalacion, name='detalle_instalacion'),
    path('inspeccion/detalle/<int:id>/', views.inspeccion_detalle, name='inspeccion_detalle'),
    path('inspecciones/todas/<int:instalacion_id>/<str:tipo>/', views.todas_inspecciones, name='todas_inspecciones'),
    path('instalacion/<int:instalacion_id>/inspeccion-mensual/nueva/', views.nueva_inspeccion_mensual, name='nueva_inspeccion_mensual'),
    path('inspeccion-mensual/update/<int:pk>/', views.update_inspeccion_mensual, name='update_inspeccion_mensual'),
    path('inspeccion-anual/update/<int:pk>/', views.update_inspeccion_anual, name='update_inspeccion_anual'),
    


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)