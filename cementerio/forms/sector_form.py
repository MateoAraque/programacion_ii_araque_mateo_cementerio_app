from django import forms

from cementerio.models import Sector


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['nombre', 'descripcion']   # explícito: nunca '__all__'
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise forms.ValidationError('El nombre no puede estar vacío.')
        return nombre
