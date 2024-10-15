from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import ControlDiario, ControlDiarioLinea
from .forms import ControlDiarioLineaForm
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.platypus import Spacer
from .models import ControlDiario, ControlDiarioLinea
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet




@login_required(login_url="/accounts/login/login")
def red_menu(request):
    return render (request, "Personal_Red/home.html")

@login_required(login_url="/accounts/login/login")
def red_menu_informes(request):
    return render (request, "Personal_Red/menu_informes.html")

@login_required(login_url="/accounts/login/login")
def informes_control_diario(request):
    controles = ControlDiario.objects.all().order_by('año', 'mes')
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





# @login_required(login_url="/accounts/login/login")
# def imprimir_control_diario(request, control_id):
#     control = ControlDiario.objects.get(id=control_id)
#     lineas = ControlDiarioLinea.objects.filter(control_diario=control).order_by('dia')

#     # Crear un objeto HttpResponse con el contenido de tipo PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="Control_Diario_{control.año}_{control.mes}.pdf"'

#     # Crear documento PDF
#     pdf = SimpleDocTemplate(response, pagesize=letter)

#     # Crear una lista para los elementos del PDF
#     elements = []

#     # Añadir imagen
#     logo_path = os.path.join(settings.BASE_DIR, 'AdminSumarteApp/static/AdminSumarteApp/img/arteixosumarte_logo_azul.png')

    
#     logo = Image(logo_path)
#     logo.drawHeight = 0.3 * inch  # Ajusta la altura según sea necesario
#     logo.drawWidth = 3 * inch  # Ajusta el ancho según sea necesario
#     elements.append(logo)
#     elements.append(Spacer(1, 12))
#     # Añadir un campo de texto para el encabezado
#     header_text = f"Control Diario - {control.año} / {control.mes}"
#     styles = getSampleStyleSheet()
#     header = Paragraph(header_text, styles['Title'])
#     elements.append(header)
    
#     # Añadir texto adicional
    
#     # Crear un estilo centrado
#     centered_style = ParagraphStyle(
#         'CenteredStyle',
#         parent=styles['Normal'],
#         alignment=1,  # 1 para centrar el texto
#         fontSize=12,
#         textColor=colors.black,
#         spaceAfter=12,
#     )
#     additional_text = "REGISTRO – CONTROL DIARIO EN DEPÓSITO Y RED (ROTANDO PUNTOS)"
#     additional_paragraph = Paragraph(additional_text, centered_style)
#     elements.append(additional_paragraph)

#     elements.append(Spacer(1, 12))  # Espaciador para separar el encabezado de la tabla

#     # Crear tabla con los datos
#     data = [['Día', 'Punto', 'Cloro Libre (≤ 1,0 ppm)', 'Cloro Comb.(≤ 2,0 ppm)', 'pH (6,5 – 9,5)', 'Turbidez (≤ 4 UNF)', 'Responsable']]
#     for linea in lineas:
#         data.append([linea.dia, linea.punto, linea.cloro_libre, linea.cloro_combinado, linea.ph, linea.turbidez, linea.responsable.username])

#     # Crear la tabla y establecer el estilo
#     table = Table(data)
#     style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ])
#     table.setStyle(style)
    
#     # Añadir estilos condicionales para los valores fuera de los parámetros
#     # Definir los límites de los parámetros
#     CLORO_LIBRE_MAX = 1.0
#     CLORO_COMBINADO_MAX = 2.0
#     PH_MIN = 6.5
#     PH_MAX = 9.5
#     TURBIDEZ_MAX = 4.0
    
#     for i, linea in enumerate(lineas, start=1):
#         if linea.cloro_libre > CLORO_LIBRE_MAX:
#             style.add('TEXTCOLOR', (2, i), (2, i), colors.red)  # Cloro Libre fuera de rango
#         if linea.cloro_combinado > CLORO_COMBINADO_MAX:
#             style.add('TEXTCOLOR', (3, i), (3, i), colors.red)  # Cloro Combinado fuera de rango
#         if not (PH_MIN <= linea.ph <= PH_MAX):
#             style.add('TEXTCOLOR', (4, i), (4, i), colors.red)  # pH fuera de rango
#         if linea.turbidez > TURBIDEZ_MAX:
#             style.add('TEXTCOLOR', (5, i), (5, i), colors.red)  # Turbidez fuera de rango

#     # Aplicar el estilo a la tabla
#     table.setStyle(style)

#     elements.append(Spacer(1, 12))  # Espaciador para separar la tabla del encabezado
#     elements.append(table)  # Agrega la tabla a los elementos

#     # Construir el PDF
#     pdf.build(elements)  # Cambia aquí para usar la lista `elements`
#     return response



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
        return render(request, 'personal_red/mi_template.html')  # O la plantilla donde quieras mostrar el formulario
