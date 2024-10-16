from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Contadores.models import CambioContador, LecturaAbonado

# Create your views here.
@login_required(login_url="/accounts/login/login")
def contadores(request):
    return render (request, "Contadores/menu_contadores.html")

@login_required(login_url="/accounts/login/login")
def cambios_contador(request):
    Cambios=CambioContador.objects.all()
    return render (request, "Contadores/cambios_contador.html",{"cambios":Cambios})

@login_required(login_url="/accounts/login/login")
def lecturas_abonados(request):
    Lecturas=LecturaAbonado.objects.all()
    return render (request, "Contadores/lecturas_abonados.html",{"lecturas":Lecturas})

