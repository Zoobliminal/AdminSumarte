#URLS APP PERSONAL_RED

from django.conf import settings
from django.conf.urls.static import static


from django.urls import path
from . import views


urlpatterns = [
    path('', views.red_menu, name='red_menu'),
    path('informes/', views.red_menu_informes, name='informes'),
    path('informes_control_diario/', views.informes_control_diario, name='informes_control_diario'),
    path('crear_control_diario/', views.crear_control_diario, name='crear_control_diario'),
    path('obtener_lineas_informe/<int:control_id>/', views.obtener_lineas_informe, name='obtener_lineas_informe'),
    path('add_linea_control_diario/<int:control_id>/', views.add_linea_control_diario, name='add_linea_control_diario'),
    path('eliminar_linea_control_diario/<int:control_id>/', views.eliminar_linea_control_diario, name='eliminar_linea_control_diario'),
    path('informes_control_diario_detalle/<int:control_id>/', views.informes_control_diario_detalle, name='informes_control_diario_detalle'),
    #path('personal_red/imprimir_control_diario/<int:control_id>/', views.imprimir_control_diario, name='imprimir_control_diario'),
    path('enviar-whatsapp/', views.enviar_whatsapp, name='enviar_whatsapp'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)