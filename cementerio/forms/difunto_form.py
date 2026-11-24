from django import forms
from django.utils import timezone

from cementerio.models import Difunto


class DifuntoForm(forms.ModelForm):
    class Meta:
        model = Difunto
        fields = ['nombres', 'apellidos', 'cedula', 'fecha_nacimiento', 'fecha_fallecimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_fallecimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula'].strip()
        if not (cedula.isascii() and cedula.isdigit() and len(cedula) == 10):
            raise forms.ValidationError('La cédula debe tener exactamente 10 dígitos numéricos.')
        return cedula

    def clean_fecha_fallecimiento(self):
        fecha = self.cleaned_data['fecha_fallecimiento']
        if fecha > timezone.localdate():
            raise forms.ValidationError('La fecha de fallecimiento no puede ser futura.')
        return fecha   # clean_<campo> siempre debe devolver el valor

    def clean(self):
        datos = super().clean()
        nacimiento = datos.get('fecha_nacimiento')
        fallecimiento = datos.get('fecha_fallecimiento')
        if nacimiento and fallecimiento and nacimiento > fallecimiento:
            raise forms.ValidationError('El nacimiento no puede ser posterior al fallecimiento.')
        return datos
