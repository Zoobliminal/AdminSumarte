from django import forms
from .models import ControlDiario, ControlDiarioLinea
import datetime
from django import forms
from .models import LineaAgenda
from Avisos.models import trabajadorAsignadoAviso

def generate_time_choices():
    times = []
    for hour in range(24):
        for minute in range(0, 60, 30):
            time = datetime.time(hour, minute)
            times.append((time.strftime('%H:%M'), time.strftime('%H:%M')))
    return times



class AgregarTareaForm(forms.ModelForm):
    class Meta:
        model = LineaAgenda
        fields = ['hora_inicio', 'hora_fin', 'descripcion']
        widgets = {
           
            'hora_inicio': forms.Select(choices=generate_time_choices(), attrs={'class': 'form-control'}),
            'hora_fin': forms.Select(choices=generate_time_choices(), attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AgregarTareaForm, self).__init__(*args, **kwargs)
        self.fields['hora_inicio'].initial = '08:00'
        self.fields['hora_fin'].initial = '09:00'


class ControlDiarioForm(forms.ModelForm):
    class Meta:
        model = ControlDiario
        fields = ['año', 'mes']
        widgets = {
            'año': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Año', 'label': 'white'}),
            'mes': forms.Select(attrs={'class': 'form-control', 'label': ''}),
        }

class ControlDiarioLineaForm(forms.ModelForm):
    class Meta:
        model = ControlDiarioLinea
        fields = ['dia','punto', 'cloro_libre', 'cloro_combinado', 'ph', 'turbidez']  # Excluir 'responsable'
        widgets = {
            'dia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Día'}),
            'punto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Punto de control'}),  
            'cloro_libre': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cloro Libre (ppm)', 'step': '0.1'}),
            'cloro_combinado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cloro Combinado (ppm)', 'step': '0.1'}),
            'ph': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nivel de pH', 'step': '0.1'}),
            'turbidez': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Turbidez (UNF)', 'step': '0.1'}),
        }

