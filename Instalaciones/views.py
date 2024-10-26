from django.contrib.auth.decorators import login_required
from .models import Instalacion
from django.shortcuts import render, get_object_or_404

from .models import Instalacion, InspeccionMensualDeposito, InspeccionAnualDeposito  # Importa los modelos



@login_required(login_url="/accounts/login/login")
def instalaciones(request):
    # Obtener todas las instalaciones
    instalaciones = Instalacion.objects.all()
    return render(request, "Instalaciones/listado_instalaciones.html", {'instalaciones': instalaciones})

@login_required(login_url="/accounts/login/login")
def mapa_instalaciones(request):
    return render (request, "Instalaciones/mapa_instalaciones.html")




def detalle_instalacion(request, instalacion_id):
    instalacion = get_object_or_404(Instalacion, id=instalacion_id)
    inspecciones_mensuales = InspeccionMensualDeposito.objects.filter(instalacion=instalacion)
    inspecciones_anuales = InspeccionAnualDeposito.objects.filter(instalacion=instalacion)
    
    context = {
        'instalacion': instalacion,
        'inspecciones_mensuales': inspecciones_mensuales,
        'inspecciones_anuales': inspecciones_anuales,
    }
    return render(request, 'Instalaciones/detalle_instalacion.html', context)