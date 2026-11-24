"""Definición de grupos y permisos. Se aplica en `migrate` y con `crear_grupos`."""
from django.contrib.auth.models import Group, Permission

from cementerio.permisos import GRUPO_ADMIN, GRUPO_CONSULTOR

MODELOS = ['sector', 'difunto', 'tumba', 'servicio']

PERMISOS_POR_GRUPO = {
    # administradores: crear, editar, eliminar y ver en las cuatro entidades
    GRUPO_ADMIN: [f'{accion}_{m}' for m in MODELOS for accion in ('add', 'change', 'delete', 'view')],
    # consultores: ver todo, y crear/editar/eliminar tumbas (editar/eliminar solo las suyas, lo valida la vista)
    GRUPO_CONSULTOR: [f'view_{m}' for m in MODELOS] + ['add_tumba', 'change_tumba', 'delete_tumba'],
}


def crear_grupos():
    for nombre, codenames in PERMISOS_POR_GRUPO.items():
        grupo, _ = Group.objects.get_or_create(name=nombre)
        permisos = Permission.objects.filter(
            content_type__app_label='cementerio', codename__in=codenames,
        )
        grupo.permissions.set(permisos)
