from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Vehiculo


class EntregablesApiTest(APITestCase):
    def test_lista_vehiculos_serializa_recurso_portado(self):
        Vehiculo.objects.create(
            patente='ABCD12',
            tipo='camion',
            marca='Volvo',
            modelo='FH',
            año=2024,
            fecha_adquisicion=date(2024, 1, 10),
        )

        response = self.client.get(reverse('entregables-vehiculo-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['patente'], 'ABCD12')
        self.assertIn('requiere_mantencion', response.data[0])
