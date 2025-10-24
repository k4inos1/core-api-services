from django.test import TestCase
from equipos.models import Equipo
from datetime import date


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
