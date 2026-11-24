from django.core.management.base import BaseCommand

from cementerio.grupos import crear_grupos


class Command(BaseCommand):
    help = 'Crea los grupos administradores y consultores con sus permisos.'

    def handle(self, *args, **options):
        crear_grupos()
        self.stdout.write(self.style.SUCCESS('Grupos creados/actualizados.'))
