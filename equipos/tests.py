from datetime import date

from django.test import TestCase
from django.urls import reverse

from equipos.models import Equipo


class EquipoModelTest(TestCase):
    def test_create_equipo(self):
        e = Equipo.objects.create(
            nombre='Proyector Epson',
            categoria='Proyector',
            estado='Operativo',
            fecha_ingreso=date.today(),
            ubicacion='Sala 201',
        )

        self.assertEqual(str(e), 'Proyector Epson')


class EquipoApiTest(TestCase):
    def test_lista_equipos_usa_serializer_drf(self):
        Equipo.objects.create(
            nombre='Notebook HP',
            categoria='Notebook',
            estado='Operativo',
            fecha_ingreso=date(2024, 3, 1),
            ubicacion='Lab 2',
        )

        response = self.client.get(reverse('equipos-list'))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['cantidad'], 1)
        self.assertEqual(payload['resultados'][0]['nombre'], 'Notebook HP')
        self.assertIn('cambios', payload['resultados'][0])
