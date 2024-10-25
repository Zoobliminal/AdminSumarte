from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
#from AdminSumarteApp.models import AgendaHoja
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from Personal_Red.models import ControlDiario, ControlDiarioLinea
from Personal_Red.forms import ControlDiarioLineaForm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer, Frame
from reportlab.pdfgen import canvas
import os

class PDFBase:
    def __init__(self, response, filename):
        self.response = response
        self.filename = filename
        self.elements = []
        self.styles = getSampleStyleSheet()

    def create_pdf(self):
        self.response['Content-Disposition'] = f'attachment; filename="{self.filename}.pdf"'
        pdf = SimpleDocTemplate(self.response, pagesize=letter)
        pdf.build(self.elements)

    def add_logo(self):
        logo_path = os.path.join(settings.BASE_DIR, 'AdminSumarteApp/static/AdminSumarteApp/img/arteixosumarte_logo_azul.png')
        logo = Image(logo_path)
        
        # Obtener dimensiones originales
        original_width = logo.imageWidth
        original_height = logo.imageHeight
        
        # Definir el nuevo ancho deseado (3 inches)
        new_width = 3 * inch
        
        # Calcular la altura manteniendo la proporción
        aspect_ratio = original_height / original_width
        new_height = new_width * aspect_ratio
        
        # Asignar las nuevas dimensiones a la imagen
        logo.drawWidth = new_width
        logo.drawHeight = new_height

        # Ajustar la posición del logo utilizando un Frame
        width, height = letter  # Tamaño de la página
        # Colocar el logo en la parte superior de la página
        logo_frame = Frame(0, height - new_height, width=new_width, height=new_height, showBoundary=0)
        
        # Añadir el logo a los elementos del PDF
        self.elements.append(logo)
        self.elements.append(Spacer(1, 12))

    def add_header(self, text):
        header = Paragraph(text, self.styles['Title'])
        self.elements.append(header)
        self.elements.append(Spacer(1, 12))


    def add_table(self, data, table_style):
        table = Table(data)
        table.setStyle(table_style)
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def add_paragraph(self, text, style_name='Normal', alignment=1):
        style = ParagraphStyle(
            style_name,
            parent=self.styles['Normal'],
            alignment=alignment,
            fontSize=12,
            textColor=colors.black,
            spaceAfter=12,
        )
        paragraph = Paragraph(text, style)
        self.elements.append(paragraph)

class PDFControlDiario(PDFBase):
    def __init__(self, response, control):
        filename = f'Control_Diario_{control.año}_{control.mes}'
        super().__init__(response, filename)
        self.control = control

    def build_pdf(self):
        # Agregar logo y encabezado
        self.add_logo()
        self.add_header(f"Control Diario - {self.control.año} / {self.control.mes}")
        self.add_paragraph("REGISTRO – CONTROL DIARIO EN DEPÓSITO Y RED (ROTANDO PUNTOS)")

        # Crear la tabla con los datos
        data = [['Día', 'Punto', 'Cloro Libre (≤ 1,0 ppm)', 'Cloro Comb.(≤ 2,0 ppm)', 'pH (6,5 – 9,5)', 'Turbidez (≤ 4 UNF)', 'Responsable']]
        lineas = ControlDiarioLinea.objects.filter(control_diario=self.control).order_by('dia')
        
        # Definir los límites de los parámetros
        CLORO_LIBRE_MAX = 1.0
        CLORO_COMBINADO_MAX = 2.0
        PH_MIN = 6.5
        PH_MAX = 9.5
        TURBIDEZ_MAX = 4.0
        
        # Estilos condicionales
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Añadir las filas con los valores
        for i, linea in enumerate(lineas, start=1):
            # Añadir la fila de datos a la tabla
            row = [
                linea.dia,
                linea.punto,
                linea.cloro_libre,
                linea.cloro_combinado,
                linea.ph,
                linea.turbidez,
                linea.responsable.username
            ]
            data.append(row)

            # Aplicar colores condicionales
            if linea.cloro_libre > CLORO_LIBRE_MAX:
                table_style.add('TEXTCOLOR', (2, i), (2, i), colors.red)  # Cloro Libre fuera de rango
            if linea.cloro_combinado > CLORO_COMBINADO_MAX:
                table_style.add('TEXTCOLOR', (3, i), (3, i), colors.red)  # Cloro Combinado fuera de rango
            if not (PH_MIN <= linea.ph <= PH_MAX):
                table_style.add('TEXTCOLOR', (4, i), (4, i), colors.red)  # pH fuera de rango
            if linea.turbidez > TURBIDEZ_MAX:
                table_style.add('TEXTCOLOR', (5, i), (5, i), colors.red)  # Turbidez fuera de rango

        # Añadir la tabla con el estilo dinámico
        self.add_table(data, table_style)

        # Generar el PDF
        self.create_pdf()