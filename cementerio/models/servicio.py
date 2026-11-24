from django.conf import settings
from django.db import models
from django.urls import reverse

from cementerio.models.tumba import Tumba


class Servicio(models.Model):
    """Trabajo realizado sobre una tumba (equivale a Prestamo)."""

    class Tipo(models.TextChoices):
        INHUMACION = 'INHUMACION', 'Inhumación'
        EXHUMACION = 'EXHUMACION', 'Exhumación'
        MANTENIMIENTO = 'MANTENIMIENTO', 'Mantenimiento'
        MISA = 'MISA', 'Misa / ceremonia'

    # CASCADE: si se elimina la tumba, su historial de servicios no tiene sentido
    tumba = models.ForeignKey(Tumba, on_delete=models.CASCADE, related_name='servicios')
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    fecha = models.DateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    responsable = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='servicios_creados',
    )

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.tumba.codigo} ({self.fecha})'

    def get_absolute_url(self):
        return reverse('servicio_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
        ordering = ['-fecha']
