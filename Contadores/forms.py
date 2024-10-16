from django import forms
from .models import CambioContador


class CambioContadorForm(forms.ModelForm):
    class Meta:
        model = CambioContador
        fields = [
            'contrato',
            'direccion',
            'numero_viejo',
            'lectura_viejo',
            'imagen_viejo',
            'numero_nuevo',
            'lectura_nuevo',
            'imagen_nuevo',
            'notas',
        ]
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3}),
        }
