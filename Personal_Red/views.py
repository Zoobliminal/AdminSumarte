# Django core imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse

# Utilities
import os
import calendar
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date

# Models and Forms
from .models import ControlDiario, ControlDiarioLinea, LineaAgenda
from .forms import ControlDiarioLineaForm, ControlDiarioForm, AgregarTareaForm

# ReportLab for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
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
def Personal_Red_menu_instalaciones(request):
    return render (request, "Personal_Red/menu_instalaciones.html")



@login_required(login_url="/accounts/login/")
def calendario_mes(request, year=None, month=None):
    
     # Obtener la fecha actual para fallback
    hoy = datetime.now()
    current_year = year if year else hoy.year
    current_month = month if month else hoy.month
    current_day = hoy.day
    fecha_completa = f"{current_year}-{int(current_month):02d}-{int(current_day):02d}"
    datetime_mes = datetime(current_year, current_month, 1)
  
    # Por defecto, seleccionamos las tareas del usuario actual
    usuario_actual = request.user

    # Si el usuario es staff, permitimos que vea las tareas de otros usuarios
    if request.user.is_staff and 'usuario_id' in request.GET:
        usuario_actual = User.objects.get(id=request.GET.get('usuario_id'))

  

    # Obtener todas las tareas del mes para el usuario seleccionado
    tareas = LineaAgenda.objects.filter(
        usuario=usuario_actual, 
        fecha_inicio__year=current_year, 
        fecha_inicio__month=current_month
    )

    # Extraer los días en los que hay tareas
    dias_con_tareas = [tarea.fecha_inicio.day for tarea in tareas]


    # Crear un calendario del mes actual
    cal = calendar.Calendar()
    weeks = cal.monthdayscalendar(current_year, current_month)


    # Calcular el mes anterior y siguiente
    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

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
    
    
    # Si el usuario es staff, pasamos también la lista de todos los usuarios
    usuarios = User.objects.all() if request.user.is_staff else None

    # Pasar los datos al contexto, incluyendo la fecha de hoy
    return render(request, 'Personal_Red/calendario_mes.html', {
        'weeks': formatted_days,
        'hoy':hoy,
        'current_year': current_year,
        'current_month': current_month,
        'current_day': current_day,
        'fecha_completa': fecha_completa,
        'datetime_mes':datetime_mes,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'dias_con_tareas': dias_con_tareas,
        'usuarios': usuarios,
        'usuario_actual': usuario_actual,  
    })




@login_required(login_url="/accounts/login/")
def calendario_dia(request, fecha):
    try:
        # Convertir el string de fecha en un objeto datetime
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    except ValueError:
        return render(request, 'error_template.html', {'error': 'Fecha inválida'})

    # Por defecto, seleccionamos las tareas del usuario actual
    usuario_actual = request.user

    # Si el usuario es staff, permitimos que vea las tareas de otros usuarios
    if request.user.is_staff and 'usuario_id' in request.GET:
        usuario_actual = User.objects.get(id=request.GET.get('usuario_id'))

    # Filtrar las tareas del usuario seleccionado (ya sea el actual o uno seleccionado por staff)
    eventos = LineaAgenda.objects.filter(usuario=usuario_actual, fecha_inicio=fecha_obj)

    ultima_tarea = LineaAgenda.objects.filter(usuario=request.user).order_by('-fecha_inicio', '-hora_fin').first()

    # Calcular día anterior y siguiente
    dia_anterior = fecha_obj - timedelta(days=1)
    dia_siguiente = fecha_obj + timedelta(days=1)


    if request.method == 'POST':
        form = AgregarTareaForm(request.POST)
        if form.is_valid():
            linea_agenda = form.save(commit=False)
            linea_agenda.usuario = request.user
            linea_agenda.fecha_inicio = fecha_obj
            linea_agenda.fecha_fin = fecha_obj
            linea_agenda.save()
            return redirect('calendario_dia', fecha=fecha)
    else:
        # Definir valores por defecto basados en la última tarea
        initial_data = {}
        if ultima_tarea:
            initial_data = {
                'hora_inicio': ultima_tarea.hora_fin,  # La hora de inicio será la hora de fin de la última tarea
                'hora_fin': (datetime.combine(fecha_obj, ultima_tarea.hora_fin) + timedelta(hours=1)).time()  # Ejemplo: Una hora más para la hora de fin
            }

        form = AgregarTareaForm(initial=initial_data)

    # Si el usuario es staff, pasamos también la lista de todos los usuarios
    usuarios = User.objects.all() if request.user.is_staff else None

    context = {
        'eventos': eventos,
        'fecha': fecha_obj,
        'form': form,
        'usuarios': usuarios,
        'usuario_actual': usuario_actual,
        'dia_anterior': dia_anterior,
        'dia_siguiente': dia_siguiente,

    }
    return render(request, 'Personal_Red/calendario_dia.html', context)



@login_required
def eliminar_linea_agenda(request, linea_id):
    # Obtener el registro específico
    linea = get_object_or_404(LineaAgenda, id=linea_id)

    # Verificar si el usuario actual es el propietario del registro
    if linea.usuario == request.user:
        # Obtener el año y mes de la tarea
        fecha = linea.fecha_inicio 
        linea.delete()

    # Redirigir al calendario del mes correspondiente
    return redirect('calendario_dia', fecha=fecha)


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
    hoy = datetime.now()
 
    return render (request, "Personal_Red/informes_control_diario.html",{'controles': page_obj,'fecha':hoy})


@login_required(login_url="/accounts/login/login")
def obtener_lineas_informe(request, control_id):
    # Asegúrate de que control_id sea un entero
    control = get_object_or_404(ControlDiario, id=control_id)
    hoy = datetime.now()
    # Filtra las líneas asociadas al control_diario especificado
    lineas = ControlDiarioLinea.objects.filter(control_diario=control).order_by('dia')

    return render(request, 'Personal_Red/informes_control_diario_detalle.html', {'lineas': lineas,'fecha':hoy, 'control': control})


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
