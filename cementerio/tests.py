from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from cementerio.grupos import crear_grupos
from cementerio.models import Sector, Tumba
from cementerio.permisos import GRUPO_ADMIN, GRUPO_CONSULTOR

User = get_user_model()


class ControlDeAccesoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        crear_grupos()
        cls.admin = User.objects.create_user('adm', password='x12345678')
        cls.admin.groups.add(Group.objects.get(name=GRUPO_ADMIN))
        cls.c1 = User.objects.create_user('c1', password='x12345678')
        cls.c1.groups.add(Group.objects.get(name=GRUPO_CONSULTOR))
        cls.c2 = User.objects.create_user('c2', password='x12345678')
        cls.c2.groups.add(Group.objects.get(name=GRUPO_CONSULTOR))
        cls.sector = Sector.objects.create(nombre='Norte', creado_por=cls.admin)
        cls.tumba = Tumba.objects.create(
            codigo='T-1', sector=cls.sector, precio=Decimal('100.00'), creado_por=cls.c1)

    def test_anonimo_va_al_login(self):
        r = self.client.get(reverse('tumba_list'))
        self.assertRedirects(r, f"{reverse('login')}?next={reverse('tumba_list')}")

    def test_id_inexistente_da_404(self):
        self.client.login(username='adm', password='x12345678')
        self.assertEqual(self.client.get(reverse('tumba_detail', args=[9999])).status_code, 404)

    def test_consultor_puede_crear_tumba(self):
        self.client.login(username='c1', password='x12345678')
        r = self.client.post(reverse('tumba_create'), {
            'codigo': 't-2', 'sector': self.sector.pk, 'estado': 'DISPONIBLE',
            'capacidad': 1, 'precio': '50.00',
        })
        self.assertRedirects(r, reverse('tumba_list'))
        nueva = Tumba.objects.get(codigo='T-2')
        self.assertEqual(nueva.creado_por, self.c1)

    def test_consultor_no_crea_sectores(self):
        self.client.login(username='c1', password='x12345678')
        self.assertEqual(self.client.get(reverse('sector_create')).status_code, 403)

    def test_propietario_edita_y_otro_consultor_no(self):
        url = reverse('tumba_update', args=[self.tumba.pk])
        self.client.login(username='c1', password='x12345678')
        self.assertEqual(self.client.get(url).status_code, 200)
        self.client.logout()
        self.client.login(username='c2', password='x12345678')
        self.assertEqual(self.client.get(url).status_code, 403)

    def test_borrado_solo_por_post(self):
        self.client.login(username='adm', password='x12345678')
        url = reverse('tumba_delete', args=[self.tumba.pk])
        self.client.get(url)
        self.assertTrue(Tumba.objects.filter(pk=self.tumba.pk).exists())
        self.client.post(url)
        self.assertFalse(Tumba.objects.filter(pk=self.tumba.pk).exists())

    def test_sector_con_tumbas_no_se_elimina(self):
        self.client.login(username='adm', password='x12345678')
        self.client.post(reverse('sector_delete', args=[self.sector.pk]))
        self.assertTrue(Sector.objects.filter(pk=self.sector.pk).exists())

    def test_logout_rechaza_get(self):
        self.client.login(username='adm', password='x12345678')
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
