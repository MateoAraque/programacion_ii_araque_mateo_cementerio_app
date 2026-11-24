from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from cementerio.grupos import crear_grupos
from cementerio.models import Difunto, Sector, Servicio, Tumba
from cementerio.permisos import GRUPO_ADMIN, GRUPO_CONSULTOR

PASSWORD = 'Cementerio2026*'


class Command(BaseCommand):
    help = 'Carga usuarios y datos de prueba (se puede ejecutar varias veces).'

    def handle(self, *args, **options):
        crear_grupos()
        User = get_user_model()

        # --- Usuarios de prueba ---
        def usuario(username, grupo=None, superuser=False):
            user, creado = User.objects.get_or_create(
                username=username, defaults={'email': f'{username}@cementerio.test'},
            )
            if creado:
                user.set_password(PASSWORD)
            if superuser:
                user.is_staff = user.is_superuser = True
            user.save()
            if grupo:
                user.groups.add(Group.objects.get(name=grupo))
            return user

        usuario('superadmin', superuser=True)
        admin = usuario('admin_cementerio', GRUPO_ADMIN)
        c1 = usuario('consultor1', GRUPO_CONSULTOR)
        c2 = usuario('consultor2', GRUPO_CONSULTOR)

        # --- Sectores (5) ---
        sectores = {}
        for nombre, desc in [
            ('Jardín del Recuerdo', 'Sepulturas en tierra con jardín.'),
            ('Nichos Norte', 'Bloque de nichos de cuatro niveles.'),
            ('Mausoleos Familiares', 'Mausoleos privados para varias personas.'),
            ('Jardín de Cenizas', 'Espacio para urnas cinerarias.'),
            ('Sector Histórico', 'Tumbas antiguas de valor patrimonial.'),
        ]:
            sectores[nombre], _ = Sector.objects.get_or_create(
                nombre=nombre, defaults={'descripcion': desc, 'creado_por': admin})

        # --- Difuntos (6) ---
        difuntos = []
        for nombres, apellidos, cedula, nac, fall, autor in [
            ('Luis', 'Andrade', '1700000001', date(1940, 3, 12), date(2019, 5, 2), admin),
            ('María', 'Benítez', '1700000002', date(1952, 7, 30), date(2021, 1, 15), admin),
            ('Carlos', 'Cevallos', '1700000003', date(1935, 11, 5), date(2018, 9, 21), c1),
            ('Rosa', 'Delgado', '1700000004', date(1948, 2, 17), date(2022, 6, 8), c1),
            ('Jorge', 'Espinoza', '1700000005', None, date(2020, 12, 1), c2),
            ('Ana', 'Fuentes', '1700000006', date(1960, 8, 9), date(2023, 3, 27), admin),
        ]:
            d, _ = Difunto.objects.get_or_create(cedula=cedula, defaults={
                'nombres': nombres, 'apellidos': apellidos, 'fecha_nacimiento': nac,
                'fecha_fallecimiento': fall, 'creado_por': autor})
            difuntos.append(d)

        # --- Tumbas (6) ---
        S = list(sectores.values())
        tumbas = []
        for i, (codigo, sector, estado, cap, precio, autor, ocupantes) in enumerate([
            ('JR-001', S[0], 'OCUPADA', 2, '850.00', admin, [0, 1]),
            ('NN-014', S[1], 'OCUPADA', 1, '600.00', c1, [2]),
            ('MF-003', S[2], 'OCUPADA', 4, '4200.00', admin, [3]),
            ('JC-020', S[3], 'OCUPADA', 1, '300.00', c2, [4]),
            ('SH-007', S[4], 'MANTENIMIENTO', 2, '1500.00', admin, [5]),
            ('JR-002', S[0], 'DISPONIBLE', 2, '850.00', c1, []),
        ]):
            t, creada = Tumba.objects.get_or_create(codigo=codigo, defaults={
                'sector': sector, 'estado': estado, 'capacidad': cap,
                'precio': Decimal(precio), 'creado_por': autor})
            if creada:
                t.difuntos.set([difuntos[j] for j in ocupantes])
            tumbas.append(t)

        # --- Servicios (6) ---
        if not Servicio.objects.exists():
            for tumba, tipo, fecha, costo, resp, autor in [
                (tumbas[0], 'INHUMACION', date(2019, 5, 3), '250.00', 'Pedro Salazar', admin),
                (tumbas[1], 'INHUMACION', date(2018, 9, 22), '200.00', 'Pedro Salazar', c1),
                (tumbas[2], 'MISA', date(2022, 6, 9), '120.00', 'Padre Manuel', admin),
                (tumbas[4], 'MANTENIMIENTO', date(2024, 2, 10), '180.00', 'Cuadrilla Norte', admin),
                (tumbas[3], 'INHUMACION', date(2020, 12, 2), '150.00', 'Juan Mora', c2),
                (tumbas[0], 'MANTENIMIENTO', date(2023, 11, 1), '90.00', 'Cuadrilla Sur', admin),
            ]:
                Servicio.objects.create(tumba=tumba, tipo=tipo, fecha=fecha,
                                        costo=Decimal(costo), responsable=resp, creado_por=autor)

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados.'))
        self.stdout.write(f'Usuarios: superadmin, admin_cementerio, consultor1, consultor2 | contraseña: {PASSWORD}')
