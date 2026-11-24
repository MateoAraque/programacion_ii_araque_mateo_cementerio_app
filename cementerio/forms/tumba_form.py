from django import forms

from cementerio.models import Tumba


class TumbaForm(forms.ModelForm):
    class Meta:
        model = Tumba
        fields = ['codigo', 'sector', 'estado', 'capacidad', 'precio', 'difuntos']
        widgets = {'difuntos': forms.CheckboxSelectMultiple}

    def clean_codigo(self):
        return self.cleaned_data['codigo'].strip().upper()

    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad < 1:
            raise forms.ValidationError('La capacidad mínima es 1.')
        return capacidad

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean(self):
        datos = super().clean()
        capacidad = datos.get('capacidad')
        difuntos = datos.get('difuntos')
        if capacidad and difuntos and difuntos.count() > capacidad:
            raise forms.ValidationError('Hay más difuntos que la capacidad de la tumba.')
        return datos
