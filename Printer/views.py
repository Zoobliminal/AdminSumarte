from django.shortcuts import render, HttpResponse
from django.template import Template, Context
from django.shortcuts import render
from AdminSumarteApp.models import AgendaHoja
from django.conf import settings
from django.contrib.auth.decorators import login_required
import datetime
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from Personal_Red.models import ControlDiario, ControlDiarioLinea
from Personal_Red.forms import ControlDiarioLineaForm
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.platypus import Spacer
from Personal_Red.models import ControlDiario, ControlDiarioLinea
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet

# Create your views here.

from django.shortcuts import render, get_object_or_404
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def imprime_control_diario(request, control_id):
    # Obtener los datos correspondientes
    control = ControlDiario.objects.get(id=control_id)
    lineas = ControlDiarioLinea.objects.filter(control_diario=control).order_by('dia')

    # Crear un objeto HttpResponse con el contenido de tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Control_Diario_{control.año}_{control.mes}.pdf"'

    # Crear documento PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Crear una lista para los elementos del PDF
    elements = []

    # Añadir imagen
    logo_path = os.path.join(settings.BASE_DIR, 'AdminSumarteApp/static/AdminSumarteApp/img/arteixosumarte_logo_azul.png')

    
    logo = Image(logo_path)
    logo.drawHeight = 0.3 * inch  # Ajusta la altura según sea necesario
    logo.drawWidth = 3 * inch  # Ajusta el ancho según sea necesario
    elements.append(logo)
    elements.append(Spacer(1, 12))
    # Añadir un campo de texto para el encabezado
    header_text = f"Control Diario - {control.año} / {control.mes}"
    styles = getSampleStyleSheet()
    header = Paragraph(header_text, styles['Title'])
    elements.append(header)
    
    # Añadir texto adicional
    
    # Crear un estilo centrado
    centered_style = ParagraphStyle(
        'CenteredStyle',
        parent=styles['Normal'],
        alignment=1,  # 1 para centrar el texto
        fontSize=12,
        textColor=colors.black,
        spaceAfter=12,
    )
    additional_text = "REGISTRO – CONTROL DIARIO EN DEPÓSITO Y RED (ROTANDO PUNTOS)"
    additional_paragraph = Paragraph(additional_text, centered_style)
    elements.append(additional_paragraph)

    elements.append(Spacer(1, 12))  # Espaciador para separar el encabezado de la tabla

    # Crear tabla con los datos
    data = [['Día', 'Punto', 'Cloro Libre (≤ 1,0 ppm)', 'Cloro Comb.(≤ 2,0 ppm)', 'pH (6,5 – 9,5)', 'Turbidez (≤ 4 UNF)', 'Responsable']]
    for linea in lineas:
        data.append([linea.dia, linea.punto, linea.cloro_libre, linea.cloro_combinado, linea.ph, linea.turbidez, linea.responsable.username])

    # Crear la tabla y establecer el estilo
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    
    # Añadir estilos condicionales para los valores fuera de los parámetros
    # Definir los límites de los parámetros
    CLORO_LIBRE_MAX = 1.0
    CLORO_COMBINADO_MAX = 2.0
    PH_MIN = 6.5
    PH_MAX = 9.5
    TURBIDEZ_MAX = 4.0
    
    for i, linea in enumerate(lineas, start=1):
        if linea.cloro_libre > CLORO_LIBRE_MAX:
            style.add('TEXTCOLOR', (2, i), (2, i), colors.red)  # Cloro Libre fuera de rango
        if linea.cloro_combinado > CLORO_COMBINADO_MAX:
            style.add('TEXTCOLOR', (3, i), (3, i), colors.red)  # Cloro Combinado fuera de rango
        if not (PH_MIN <= linea.ph <= PH_MAX):
            style.add('TEXTCOLOR', (4, i), (4, i), colors.red)  # pH fuera de rango
        if linea.turbidez > TURBIDEZ_MAX:
            style.add('TEXTCOLOR', (5, i), (5, i), colors.red)  # Turbidez fuera de rango

    # Aplicar el estilo a la tabla
    table.setStyle(style)

    elements.append(Spacer(1, 12))  # Espaciador para separar la tabla del encabezado
    elements.append(table)  # Agrega la tabla a los elementos

    # Construir el PDF
    pdf.build(elements)  # Cambia aquí para usar la lista `elements`
    return response
