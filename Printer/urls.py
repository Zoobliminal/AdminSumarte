#URLS APP PERSONAL_RED

from django.conf import settings
from django.conf.urls.static import static


from django.urls import path
from . import views

urlpatterns = [
    path('control-diario/<int:control_id>/', views.imprime_control_diario, name='imprime_control_diario'),
    #path('otro-informe/<int:id>/', views.imprimir_otro_informe, name='imprimir_otro_informe'),
    # Agrega más rutas según sea necesario
]

# linea para la configuracion de la url de los archivos media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 #Recuerda que Django solo sirve archivos estáticos y multimedia en el modo de desarrollo (DEBUG = True). 
 #Asegúrate de que en tu archivo settings.py esté configurado así: 