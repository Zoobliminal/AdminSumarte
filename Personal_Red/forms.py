from django import forms
from .models import ControlDiario, ControlDiarioLinea

from django import forms
from .models import LineaAgenda
from Avisos.models import trabajadorAsignadoAviso

class LineaAgendaForm(forms.ModelForm):
    direccion_aviso = forms.ModelChoiceField(
        queryset=None,  # Lo filtraremos en __init__
        required=False,
        label='Dirección del Aviso',
        help_text="Selecciona una dirección de los avisos asignados"
    )

    class Meta:
        model = LineaAgenda
        fields = ['fecha_inicio', 'fecha_fin', 'hora_inicio', 'hora_fin', 'descripcion', 'direccion_aviso']

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        if usuario:
            # Filtrar los avisos asignados al usuario actual
            self.fields['direccion_aviso'].queryset = trabajadorAsignadoAviso.objects.filter(trabajador=usuario).select_related('aviso')
        
    def save(self, commit=True):
        evento = super().save(commit=False)
        aviso = self.cleaned_data.get('direccion_aviso')
        
        # Agregar la dirección del aviso a la descripción si se seleccionó
        if aviso:
            evento.descripcion = f"{evento.descripcion} - {aviso.aviso.direccion}"  # Asegúrate de que el modelo Aviso tiene un campo 'direccion'
        
        if commit:
            evento.save()
        return evento


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

