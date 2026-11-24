from django.conf import settings
from django.db import models
from django.urls import reverse


class Difunto(models.Model):
    """Persona sepultada (equivale a Autor en biblioteca-app)."""
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_fallecimiento = models.DateField()
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='difuntos_creados',
    )

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'

    def get_absolute_url(self):
        return reverse('difunto_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'difunto'
        verbose_name_plural = 'difuntos'
        ordering = ['apellidos', 'nombres']
