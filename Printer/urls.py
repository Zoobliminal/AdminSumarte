from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('control-diario/<int:control_id>/', views.imprime_control_diario, name='imprime_control_diario'),
    
    #path('otro-informe/<int:id>/', views.imprimir_otro_informe, name='imprimir_otro_informe'),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)