from django.test import TestCase
from datetime import date
from typing import cast, Any, Dict

from .models import Equipo, CambioEquipo
from . import services


class ServiciosEquiposTest(TestCase):
    def test_reg_traza(self):
        data: Dict[str, Any] = {
            'nombre': 'Test Equipo 1',
            'categoria': 'Notebook',
            'estado': 'Operativo',
            'fecha_ingreso': date.today(),
            'ubicacion': 'Sala 1',
        }
        equipo = services.registrar_equipo(data)
        self.assertIsInstance(equipo, Equipo)
        actualizado = cast(Equipo, services.actualizar_equipo(
            cast(int, getattr(equipo, 'id')), {'ubicacion': 'Sala 2'}, usuario='tester'))
        self.assertIsInstance(actualizado, Equipo)
        self.assertEqual(actualizado.ubicacion, 'Sala 2')
        cambios = CambioEquipo.objects.filter(
            equipo=equipo, modified_field='ubicacion')
        self.assertTrue(cambios.exists())
        e = services.registrar_equipo(
            {
                'nombre': 'Equipo Baja',
                'categoria': 'Impresora',
                'estado': 'Operativo',
                'fecha_ingreso': date.today(),
                'ubicacion': 'Sala X',
            }
        )
        services.dar_de_baja_equipo(
            cast(int, getattr(e, 'id')), usuario='admin')
        e.refresh_from_db()
        self.assertEqual(e.estado, 'Dado de baja')
        services.eliminar_equipo(cast(int, getattr(e, 'id')), usuario='admin')
        self.assertFalse(Equipo.objects.filter(
            id=cast(int, getattr(e, 'id'))).exists())
