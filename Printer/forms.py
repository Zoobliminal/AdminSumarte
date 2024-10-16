# forms.py
from django import forms
from .models import ControlDiario

class ControlDiarioForm(forms.ModelForm):
    class Meta:
        model = ControlDiario  # Asegúrate de usar tu modelo correcto
        fields = ['año', 'mes']  # Cambia los campos según tu modelo
