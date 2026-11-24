from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _crear_grupos(sender, **kwargs):
    """Al terminar `migrate`, los grupos y sus permisos quedan creados."""
    from cementerio.grupos import crear_grupos
    crear_grupos()


class CementerioConfig(AppConfig):
    name = 'cementerio'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        post_migrate.connect(_crear_grupos, sender=self, dispatch_uid='cementerio_crear_grupos')
