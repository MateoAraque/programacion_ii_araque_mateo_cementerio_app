"""Reglas de acceso reutilizables por las vistas."""
GRUPO_ADMIN = 'administradores'
GRUPO_CONSULTOR = 'consultores'


def es_administrador(user):
    return user.is_superuser or user.groups.filter(name=GRUPO_ADMIN).exists()


def puede_modificar(user, obj):
    """Regla de propiedad: el administrador puede todo; el resto, solo lo que creó."""
    if es_administrador(user):
        return True
    return obj.creado_por_id is not None and obj.creado_por_id == user.id


def marcar_propiedad(user, objetos):
    """Añade `puede_modificar` a cada objeto para usarlo en las plantillas (una sola consulta de grupo)."""
    admin = es_administrador(user)
    for obj in objetos:
        obj.puede_modificar = admin or (obj.creado_por_id is not None and obj.creado_por_id == user.id)
    return objetos
