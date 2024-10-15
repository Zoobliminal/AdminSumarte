from django import forms
from .models import ControlDiario, ControlDiarioLinea

class ControlDiarioForm(forms.ModelForm):
    class Meta:
        model = ControlDiario
        fields = ['año', 'mes']
        widgets = {
            'año': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Año'}),
            'mes': forms.Select(attrs={'class': 'form-control'}),
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

