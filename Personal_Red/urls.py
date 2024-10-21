#URLS APP PERSONAL_RED

from django.conf import settings
from django.conf.urls.static import static


from django.urls import path
from . import views


urlpatterns = [
    path('', views.Personal_Red_menu_principal, name='red'),

    path('calendario_mes/<int:year>/<int:month>/', views.calendario_mes, name='calendario_mes'),
    path('calendario_dia/<str:fecha>/', views.calendario_dia, name='calendario_dia'),
    path('informes/', views.Personal_Red_menu_informes, name='informes'),
    path('informes_control_diario/', views.informes_control_diario, name='informes_control_diario'),
    path('crear_control_diario/', views.crear_control_diario, name='crear_control_diario'),
    path('obtener_lineas_informe/<int:control_id>/', views.obtener_lineas_informe, name='obtener_lineas_informe'),
    path('add_linea_control_diario/<int:control_id>/', views.add_linea_control_diario, name='add_linea_control_diario'),
    path('eliminar_linea_control_diario/<int:control_id>/', views.eliminar_linea_control_diario, name='eliminar_linea_control_diario'),
    path('informes_control_diario_detalle/<int:control_id>/', views.informes_control_diario_detalle, name='informes_control_diario_detalle'),


    
    path('enviar-whatsapp/', views.enviar_whatsapp, name='enviar_whatsapp'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)