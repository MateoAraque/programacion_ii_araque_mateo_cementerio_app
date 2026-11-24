from django.contrib import admin

from cementerio.models import Difunto, Sector, Servicio, Tumba


class AutoriaAdmin(admin.ModelAdmin):
    """Asigna creado_por automáticamente al crear desde el admin."""

    def save_model(self, request, obj, form, change):
        if not change and obj.creado_por is None:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Sector)
class SectorAdmin(AutoriaAdmin):
    list_display = ('nombre', 'descripcion', 'creado_por')
    list_filter = ('creado_por',)
    search_fields = ('nombre', 'descripcion')


@admin.register(Difunto)
class DifuntoAdmin(AutoriaAdmin):
    list_display = ('apellidos', 'nombres', 'cedula', 'fecha_fallecimiento')
    list_filter = ('fecha_fallecimiento',)
    search_fields = ('nombres', 'apellidos', 'cedula')


@admin.register(Tumba)
class TumbaAdmin(AutoriaAdmin):
    list_display = ('codigo', 'sector', 'estado', 'capacidad', 'precio')
    list_filter = ('estado', 'sector')
    search_fields = ('codigo', 'sector__nombre', 'difuntos__apellidos')
    filter_horizontal = ('difuntos',)


@admin.register(Servicio)
class ServicioAdmin(AutoriaAdmin):
    list_display = ('tumba', 'tipo', 'fecha', 'costo', 'responsable')
    list_filter = ('tipo', 'fecha')
    search_fields = ('tumba__codigo', 'responsable')
