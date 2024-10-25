from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/accounts/login/login")
def instalaciones(request):
    return render (request, "Instalaciones/listado_instalaciones.html")

@login_required(login_url="/accounts/login/login")
def mapa_instalaciones(request):
    return render (request, "Instalaciones/mapa_instalaciones.html")