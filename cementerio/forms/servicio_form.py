from django import forms

from cementerio.models import Servicio


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['tumba', 'tipo', 'fecha', 'costo', 'responsable', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_costo(self):
        costo = self.cleaned_data['costo']
        if costo < 0:
            raise forms.ValidationError('El costo no puede ser negativo.')
        return costo
