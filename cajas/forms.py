from django import forms
from .models import Caja, TipoCaja
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UsernameField

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

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if empresa:
            self.fields['tipo_caja'].queryset = TipoCaja.objects.filter(
                empresa=empresa,
                activo=True
            ).order_by('nombre')
        else:
            self.fields['tipo_caja'].queryset = TipoCaja.objects.none()
            
            
class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password',
        }),
    )            