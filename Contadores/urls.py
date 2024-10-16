#URLS APP CONTADORES

from django.urls import path
from . import views


urlpatterns = [
    path('', views.contadores, name="contadores"),
    path('registrar_cambio_contador/', views.registrar_cambio_contador, name='registrar_cambio_contador'),
    path('cambios_contador/', views.cambios_contador, name="cambios_contador"),
    path('lecturas_abonados/', views.lecturas_abonados, name="lecturas_abonados"),
    

]





