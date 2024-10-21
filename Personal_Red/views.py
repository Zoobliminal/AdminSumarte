from django.conf import settings
import os
import calendar
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from django.urls import reverse 
from .models import ControlDiario, ControlDiarioLinea, LineaAgenda
from .forms import ControlDiarioLineaForm, ControlDiarioForm,LineaAgendaForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.platypus import Spacer
from reportlab.pdfgen import canvas



@login_required(login_url="/accounts/login/login")
def Personal_Red_menu_principal(request):
    
    now = datetime.now()
    año_actual = now.year
    mes_actual = now.month
    
    return render(request, 'Personal_Red/Personal_Red_menu_principal.html', {
        'year': año_actual,
        'month': mes_actual,
    })


@login_required(login_url="/accounts/login/login")
def Personal_Red_menu_informes(request):
    return render (request, "Personal_Red/menu_informes.html")


@login_required(login_url="/accounts/login/login")
def calendario(request):
    return render (request, "Personal_Red/calendario_mes.html")



@login_required(login_url="/accounts/login/")
def calendario_mes(request, year, month):
    
    # Obtener la fecha de hoy
    hoy = datetime.now()
    current_year = hoy.year
    current_month = hoy.month
    current_day = hoy.day

    # Crear un calendario del mes actual
    cal = calendar.Calendar()
    weeks = cal.monthdayscalendar(current_year, current_month)

    # Convertir cada día en la semana en un objeto de fecha, excluyendo los días vacíos (0)
    formatted_days = []
    for week in weeks:
        formatted_week = []
        for day in week:
            if day != 0:  # Excluyendo los días fuera del mes (0)
                formatted_day = f"{current_year}-{current_month:02d}-{day:02d}"  # Formato "YYYY-MM-DD"
                formatted_week.append(formatted_day)
            else:
                formatted_week.append(None)
        formatted_days.append(formatted_week)


    # Pasar los datos al contexto, incluyendo la fecha de hoy
    return render(request, 'Personal_Red/calendario_mes.html', {
        'weeks': formatted_days,
        'current_year': current_year,
        'current_month': current_month,
        'current_day': current_day,
    
    })






@login_required(login_url="/accounts/login/")
def calendario_dia(request, fecha):
    try:
        # Convertir el string de fecha en un objeto datetime
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    except ValueError:
        # Si la fecha no es válida, mostrar un error
        return render(request, 'error_template.html', {'error': 'Fecha inválida'})

    # Filtrar las tareas del usuario para la fecha seleccionada
    tareas = LineaAgenda.objects.filter(usuario=request.user, fecha_inicio=fecha)

    return render(request, 'Personal_Red/calendario_dia.html', {
        'tareas': tareas,
        'fecha': fecha,
    })


def crear_control_diario(request):
    if request.method == 'POST':
        form = ControlDiarioForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo control diario en la base de datos
            form.save()
            # Redirigir a la lista de controles diarios después de crear uno nuevo
            return redirect(reverse('informes_control_diario'))  # Cambia el nombre a la vista que maneja la lista
    else:
        form = ControlDiarioForm()

    controles = ControlDiario.objects.all().order_by('-año', '-mes')    
    return render(request, 'Personal_Red/crear_control_diario.html', {'form': form})



@login_required(login_url="/accounts/login/login")
def informes_control_diario(request):
    controles = ControlDiario.objects.all().order_by('-año', '-mes')
    paginator = Paginator(controles, 12)  # 12 controles por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    return render (request, "Personal_Red/informes_control_diario.html",{'controles': page_obj})


@login_required(login_url="/accounts/login/login")
def obtener_lineas_informe(request, control_id):
    # Asegúrate de que control_id sea un entero
    control = get_object_or_404(ControlDiario, id=control_id)
    
    # Filtra las líneas asociadas al control_diario especificado
    lineas = ControlDiarioLinea.objects.filter(control_diario=control).order_by('dia')

    return render(request, 'Personal_Red/informes_control_diario_detalle.html', {'lineas': lineas, 'control': control})


@login_required(login_url="/accounts/login/login")
def add_linea_control_diario(request, control_id):
    control_diario = ControlDiario.objects.get(id=control_id) # Obtener el control diario por ID
    if request.method == 'POST':
        form = ControlDiarioLineaForm(request.POST)
        if form.is_valid():
            linea = form.save(commit=False)
            linea.control_diario = control_diario  # Asociar la línea al control diario
            linea.responsable = request.user  # Establecer el responsable como el usuario actual
            linea.save()
            return redirect('informes_control_diario_detalle', control_id=control_id)
    else:
        form = ControlDiarioLineaForm()
    
    return render(request, 'Personal_Red/add_linea_control_diario.html', {'form': form, 'control_diario': control_diario})



@login_required
def eliminar_linea_control_diario(request, control_id):
    if request.method == 'POST':
        dia = request.POST.get('dia')

        # Buscar la línea de control diario correspondiente
        linea = get_object_or_404(ControlDiarioLinea, control_diario_id=control_id, dia=dia)
        
        # Eliminar la línea si se encuentra
        linea.delete()
        messages.success(request, f"El día {dia} ha sido eliminado exitosamente.")
        
        return redirect('informes_control_diario_detalle', control_id)

    # En caso de que no sea POST, redirige de vuelta al detalle del control
    return redirect('informes_control_diario_detalle', control_id)



@login_required(login_url="/accounts/login/login")
def informes_control_diario_detalle(request, control_id):
    control = ControlDiario.objects.get(id=control_id)
    lineas = ControlDiarioLinea.objects.filter(control_diario=control)
    return render(request, 'Personal_Red/informes_control_diario_detalle.html', {'control': control, 'lineas': lineas})







from django.shortcuts import render, redirect
from django.contrib import messages
from twilio.rest import Client
from django.conf import settings

def enviar_whatsapp(request):
    if request.method == 'POST':
        # Credenciales de Twilio (pueden venir de variables de entorno o directamente en settings)
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN

        # Crear cliente Twilio
        client = Client(account_sid, auth_token)

        # Crear el mensaje
        try:
            message = client.messages.create(
                body='Hola, esta es una notificacion de prueba desde Twilio WhatsApp Sandbox',
                from_='whatsapp:+14155238886',  # Número de WhatsApp de Twilio
                to='whatsapp:+34680438625'  # Tu número registrado en formato internacional
            )
            messages.success(request, f"Mensaje enviado exitosamente con SID: {message.sid}")
        except Exception as e:
            messages.error(request, f"Error al enviar el mensaje: {e}")
        
        # Redirigir o renderizar el template
        return redirect('informes')  # O el nombre de la vista a la que deseas redirigir
    else:
        return render(request, 'Personal_Red/mi_template.html')  # O la plantilla donde quieras mostrar el formulario
