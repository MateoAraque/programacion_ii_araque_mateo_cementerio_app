from django.conf import settings
from django.db import models
from django.urls import reverse

from cementerio.models.difunto import Difunto
from cementerio.models.sector import Sector


class Tumba(models.Model):
    """Espacio de sepultura (entidad principal, equivale a Libro)."""

    class Estado(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        OCUPADA = 'OCUPADA', 'Ocupada'
        MANTENIMIENTO = 'MANTENIMIENTO', 'En mantenimiento'

    codigo = models.CharField(max_length=20, unique=True)
    # PROTECT: no se puede borrar un sector que aún tiene tumbas
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name='tumbas')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.DISPONIBLE)
    capacidad = models.PositiveSmallIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)   # dinero => Decimal
    difuntos = models.ManyToManyField(Difunto, related_name='tumbas', blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tumbas_creadas',
    )

    def __str__(self):
        return f'{self.codigo} ({self.sector})'

    def get_absolute_url(self):
        return reverse('tumba_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'tumba'
        verbose_name_plural = 'tumbas'
        ordering = ['codigo']
