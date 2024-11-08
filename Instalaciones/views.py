from django.contrib.auth.decorators import login_required
from .models import Instalacion
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Instalacion, InspeccionMensualDeposito, InspeccionAnualDeposito  # Importa los modelos



@login_required(login_url="/accounts/login/login")
def instalaciones(request):
    # Obtener todas las instalaciones
    instalaciones = Instalacion.objects.all()
    return render(request, "Instalaciones/listado_instalaciones.html", {'instalaciones': instalaciones})

@login_required(login_url="/accounts/login/login")
def mapa_instalaciones(request):
    return render (request, "Instalaciones/mapa_instalaciones.html")




@login_required(login_url="/accounts/login/login")
def detalle_instalacion(request, instalacion_id):
    instalacion = get_object_or_404(Instalacion, id=instalacion_id)
    inspecciones_mensuales = InspeccionMensualDeposito.objects.filter(instalacion=instalacion).order_by('-fecha_realizada')
    inspecciones_anuales = InspeccionAnualDeposito.objects.filter(instalacion=instalacion).order_by('-fecha_realizada')
    
    # Obtener solo la última inspección mensual y anual
    ultima_inspeccion_mensual = inspecciones_mensuales.first()  # Esto obtendrá la primera (más reciente)
    ultima_inspeccion_anual = inspecciones_anuales.first()      # Esto obtendrá la primera (más reciente)
    
    context = {
        'instalacion': instalacion,
        'inspecciones_mensuales': inspecciones_mensuales,
        'inspecciones_anuales': inspecciones_anuales,
        'ultima_inspeccion_mensual': ultima_inspeccion_mensual,
        'ultima_inspeccion_anual': ultima_inspeccion_anual,
    }
    return render(request, 'Instalaciones/detalle_instalacion.html', context)



def inspeccion_detalle(request, id):
    inspeccion = get_object_or_404(Inspeccion, id=id)
    return render(request, 'Instalaciones/inspeccion_detalle.html', {'inspeccion': inspeccion})

def todas_inspecciones(request, instalacion_id, tipo):
    inspecciones = Inspeccion.objects.filter(instalacion_id=instalacion_id, tipo=tipo)
    return render(request, 'AdminSumarteApp/todas_inspecciones.html', {'inspecciones': inspecciones})


def update_inspeccion_mensual(request, pk):
    inspeccion = get_object_or_404(InspeccionMensualDeposito, pk=pk)
    if request.method == 'POST':
        fecha_realizada = request.POST.get('fecha_realizada')
        if fecha_realizada:
            inspeccion.fecha_realizada = fecha_realizada
        inspeccion.elementos_cierre = 'elementos_cierre' in request.POST
        inspeccion.senalizacion = 'senalizacion' in request.POST
        inspeccion.estado_valvulas = 'estado_valvulas' in request.POST
        inspeccion.canalizaciones = 'canalizaciones' in request.POST
        inspeccion.instalaciones = 'instalaciones' in request.POST
        inspeccion.observaciones = request.POST.get('observaciones')
        inspeccion.save()
        messages.success(request, "Inspección mensual actualizada correctamente.")
        return redirect('detalle_instalacion', instalacion_id=inspeccion.instalacion.pk)
    
def update_inspeccion_anual(request, pk):
    inspeccion = get_object_or_404(InspeccionAnualDeposito, pk=pk)
    if request.method == 'POST':
        fecha_realizada = request.POST.get('fecha_realizada')
        if fecha_realizada:
            inspeccion.fecha_realizada = fecha_realizada
        
        inspeccion.revision_fisuras = request.POST.get('revision_fisuras')
        inspeccion.revision_corrosion = request.POST.get('revision_corrosion')
        inspeccion.revision_materiales_sellado = request.POST.get('revision_materiales_sellado')
        inspeccion.revision_paramentos_exteriores = request.POST.get('revision_paramentos_exteriores')
        inspeccion.existencia_sedimentos = request.POST.get('existencia_sedimentos')
        inspeccion.observaciones = request.POST.get('observaciones')
        inspeccion.save()
        messages.success(request, "Inspección anual actualizada correctamente.")
        return redirect('detalle_instalacion', instalacion_id=inspeccion.instalacion.pk)