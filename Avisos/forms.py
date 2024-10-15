from django import forms
from .models import imageComentAviso, trabajadorAsignadoAviso, Aviso
from django.contrib.auth.models import User 

class NuevoAvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = [
            #'Usuario',
            'contrato',
            'nombre',
            'telefono',
            'registro',
            'direccion',
            'motivo',
            'modo',
         
        ]
        widgets = {
            #'Usuario': forms.Select(attrs={'class': 'form-control'}),
            'contrato': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'registro': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'modo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class formImageComentAviso(forms.ModelForm):
    class Meta:
        model = imageComentAviso
        fields = ['comentario', 'imagen']  # Campos editables por el usuario



class AsignarTrabajadorForm(forms.ModelForm):
    trabajador = forms.ModelChoiceField(
    queryset=User.objects.filter(groups__name='Trabajadores'),
    empty_label="Selecciona un trabajador",
    widget=forms.Select(attrs={'class': 'form-control'})  # Clase CSS para estilizar el select
   
    )
   
    class Meta:
        model = trabajadorAsignadoAviso
        fields = ['trabajador']



class editarAvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['registro','contrato','nombre','telefono','direccion', 'motivo', 'modo',]