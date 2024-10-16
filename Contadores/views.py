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

def registrar_cambio_contador(request):
    if request.method == 'POST':
        #form = ControlDiarioForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo control diario en la base de datos
            form.save()
            # Redirigir a la lista de controles diarios después de crear uno nuevo
            return redirect(reverse('Contadores/cambios_contador.html'))  # Cambia el nombre a la vista que maneja la lista
    else:
        form = ControlDiarioForm()

    controles = ControlDiario.objects.all().order_by('-año', '-mes')    
    return render(request, 'Contadores/registrar_cambio_contador.html', {'form': form})

