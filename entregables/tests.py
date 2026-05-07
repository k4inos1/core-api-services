from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Vehiculo, Operario, Faena
from datetime import date, timedelta

class SeguridadTestCase(TestCase):
    def setUp(self):
        # Crear usuario para pruebas
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        
    def test_acceso_protegido(self):
        """Prueba que las vistas requieren login"""
        response = self.client.get(reverse('index'))
        # Debe redirigir al login (302)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_acceso_autorizado(self):
        """Prueba acceso con usuario logueado"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class ValidacionModelosTestCase(TestCase):
    def test_validacion_rut(self):
        """Prueba la validación de RUT chileno"""
        # RUT válido
        self.assertTrue(Operario.validar_rut('12.345.678-5'))
        self.assertTrue(Operario.validar_rut('12345678-5'))
        self.assertTrue(Operario.validar_rut('123456785'))
        
        # RUT inválido
        self.assertFalse(Operario.validar_rut('12.345.678-K')) # DV incorrecto
        self.assertFalse(Operario.validar_rut('invalid-rut')) # Formato incorrecto

    def test_creacion_vehiculo(self):
        """Prueba la creación y validaciones de vehículo"""
        vehiculo = Vehiculo.objects.create(
            patente='ABCD-12',
            tipo='camion',
            marca='Volvo',
            modelo='FH',
            año=2020,
            estado='operativo',
            horas_uso=100,
            fecha_adquisicion=date.today()
        )
        self.assertEqual(vehiculo.patente, 'ABCD-12')
        self.assertFalse(vehiculo.requiere_mantencion())
        
        # Simular uso para requerir mantención
        vehiculo.horas_uso = 500
        vehiculo.save()
        self.assertTrue(vehiculo.requiere_mantencion())

class FlujoFaenaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='password123')
        self.client.login(username='admin', password='password123')
        
        self.vehiculo = Vehiculo.objects.create(
            patente='TEST-01', tipo='skidder', marca='CAT', modelo='525',
            año=2021, fecha_adquisicion=date.today()
        )
        self.operario = Operario.objects.create(
            rut='11111111-1', nombre='Juan Perez', rol='operador',
            fecha_ingreso=date.today()
        )

    def test_crear_faena(self):
        """Prueba el flujo de creación de una faena"""
        data = {
            'nombre': 'Corte Sector Norte',
            'tipo': 'corta',
            'ubicacion': 'Predio Los Pinos',
            'vehiculo': self.vehiculo.id,
            'operario': self.operario.id,
            'estado': 'planificada',
            'fecha_inicio': date.today(),
            'metros_cubicos': 500
        }
        response = self.client.post(reverse('faena_create'), data)
        self.assertEqual(response.status_code, 302) # Redirección exitosa
        
        # Verificar que se creó
        self.assertTrue(Faena.objects.filter(nombre='Corte Sector Norte').exists())
