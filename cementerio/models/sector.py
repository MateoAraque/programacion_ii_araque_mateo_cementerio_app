from django.conf import settings
from django.db import models
from django.urls import reverse


class Sector(models.Model):
    """Zona del cementerio (equivale a Categoria en biblioteca-app)."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    # SET_NULL: si se borra el usuario, el registro se conserva
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sectores_creados',
    )

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('sector_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'sector'
        verbose_name_plural = 'sectores'
        ordering = ['nombre']
