from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    # path('gestion_corte/', views.gestion_corte, name="gestion_corte"),
    # path('calendario_jornada/', views.calendario_jornada, name="calendario_jornada"),
    # path('busca_hoja_jornada/', views.busca_hoja_jornada, name="busca_hoja_jornada"),
    # path('fichaje/', views.fichaje, name="fichaje"),
]

# linea para la configuracion de la url de los archivos media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 #Recuerda que Django solo sirve archivos estáticos y multimedia en el modo de desarrollo (DEBUG = True). 
 #Asegúrate de que en tu archivo settings.py esté configurado así: 