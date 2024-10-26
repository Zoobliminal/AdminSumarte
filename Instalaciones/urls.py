#URLS APP INSTALACIONES

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.instalaciones, name='instalaciones'),
    path('mapa/', views.mapa_instalaciones, name='mapa_instalaciones'),
    path('instalacion/<int:instalacion_id>/', views.detalle_instalacion, name='detalle_instalacion'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)