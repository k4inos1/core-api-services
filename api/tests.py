from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from .constants import CategoriaEquipo
from .models import Equipo


class ApiViewSetTest(APITestCase):
    def test_lista_equipos_expuestos_por_api_portada(self):
        Equipo.objects.create(
            nombre='Bomba Principal',
            empresa_nombre='Forestal Demo',
            categoria=CategoriaEquipo.MECANICO,
            es_critico=True,
            numero_serie='EV4-001',
            ubicacion='Planta 1',
            fecha_instalacion=timezone.now() - timedelta(days=30),
        )

        response = self.client.get(reverse('api-equipo-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['numero_serie'], 'EV4-001')
        self.assertEqual(response.data[0]['categoria_display'], 'Mecánico')
