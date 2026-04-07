from django import forms
from .models import Caja, TipoCaja


class TipoCajaForm(forms.ModelForm):
    class Meta:
        model = TipoCaja
        fields = ['nombre', 'prefijo', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: NAPS'
            }),
            'prefijo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: NAPS'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['tipo_caja', 'tecnico', 'ubicacion', 'descripcion']
        widgets = {
            'tipo_caja': forms.Select(attrs={'class': 'form-select'}),
            'tecnico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del técnico'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observación o descripción'
            }),
        }