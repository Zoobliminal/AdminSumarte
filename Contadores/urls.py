#URLS APP CONTADORES

from django.urls import path
from . import views


urlpatterns = [
    path('', views.cambios_contador, name="Contadores"),
    path('cambios_contador/', views.cambios_contador, name="cambios_contador"),
    path('lecturas_abonados/', views.lecturas_abonados, name="lecturas_abonados"),
    

]
