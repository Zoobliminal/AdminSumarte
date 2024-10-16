# Printer/views.py
from django.http import HttpResponse
from .utils.pdf_generator import PDFControlDiario
from Personal_Red.models import ControlDiario
from django.shortcuts import render, redirect
from django.urls import reverse
from Personal_Red.forms import ControlDiarioForm  # Asegúrate de importar tu formulario





def imprime_control_diario(request, control_id):
    control = ControlDiario.objects.get(id=control_id)
    response = HttpResponse(content_type='application/pdf')
    
    # Usar la clase derivada para crear el PDF
    pdf = PDFControlDiario(response, control)
    pdf.build_pdf()

    return response
