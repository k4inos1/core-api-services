from django.core.management.base import BaseCommand
from entregables.models import Vehiculo, Operario, Faena, Mantencion, RegistroIncidente
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Poblar la base de datos con un GRAN volumen de datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando población MASIVA de datos...')

        # 1. Crear Vehículos (50)
        tipos_vehiculo = ['camion', 'cosechadora', 'skidder', 'grua', 'camioneta', 'excavadora']
        marcas = ['Volvo', 'Mercedes-Benz', 'Caterpillar', 'John Deere', 'Komatsu', 'Scania', 'MAN', 'Tigercat']
        
        vehiculos = []
        for i in range(50):
            patente = f'BIG-{i:03d}'
            if not Vehiculo.objects.filter(patente=patente).exists():
                v = Vehiculo.objects.create(
                    patente=patente,
                    tipo=random.choice(tipos_vehiculo),
                    marca=random.choice(marcas),
                    modelo=f'Modelo-{random.randint(1000, 9999)}',
                    año=random.randint(2010, 2025),
                    estado=random.choice(['operativo', 'operativo', 'operativo', 'en_mantencion', 'fuera_servicio']),
                    horas_uso=random.randint(0, 15000),
                    fecha_adquisicion=timezone.now().date() - timedelta(days=random.randint(0, 3000)),
                    fecha_creacion=timezone.now() - timedelta(days=random.randint(0, 3000)), # Fecha registro histórico
                    activo=True
                )
                vehiculos.append(v)
                if i % 10 == 0: self.stdout.write(f'Vehículo creado: {v.patente}')
            else:
                vehiculos.append(Vehiculo.objects.get(patente=patente))

        # 2. Crear Operarios (50)
        roles = ['operador', 'chofer', 'mecanico', 'supervisor', 'jefe_cuadrilla']
        nombres = ['Juan', 'Pedro', 'Luis', 'Carlos', 'Ana', 'Maria', 'Jose', 'Miguel', 'Roberto', 'Diego', 'Sofia', 'Camila', 'Valentina', 'Isabella']
        apellidos = ['Perez', 'Gonzalez', 'Rodriguez', 'Lopez', 'Martinez', 'Sanchez', 'Fernandez', 'Torres', 'Ramirez', 'Diaz', 'Muñoz', 'Rojas']

        operarios = []
        for i in range(50):
            # Generar RUT único
            rut = f'{random.randint(5, 30)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(0, 9)}'
            if not Operario.objects.filter(rut=rut).exists():
                o = Operario.objects.create(
                    rut=rut,
                    nombre=f'{random.choice(nombres)} {random.choice(apellidos)}',
                    rol=random.choice(roles),
                    licencia=random.choice(['A1', 'A2', 'A3', 'A4', 'A5', 'D', 'B']),
                    fecha_ingreso=timezone.now().date() - timedelta(days=random.randint(0, 4000)),
                    activo=True
                )
                operarios.append(o)
                if i % 10 == 0: self.stdout.write(f'Operario creado: {o.nombre}')
            else:
                pass
        
        operarios = list(Operario.objects.all())

        # 3. Crear Faenas (100)
        tipos_faena = ['corta', 'transporte', 'plantacion', 'raleo', 'limpieza']
        ubicaciones = ['Sector Los Pinos', 'Fundo El Roble', 'Predio San José', 'Lote 45', 'Cerro Alto', 'Valle Verde', 'Rio Claro', 'La Esperanza']
        
        faenas = []
        if vehiculos and operarios:
            for i in range(100):
                f = Faena.objects.create(
                    nombre=f'Faena {random.choice(tipos_faena).capitalize()} {i+1}',
                    tipo=random.choice(tipos_faena),
                    ubicacion=random.choice(ubicaciones),
                    vehiculo=random.choice(vehiculos),
                    operario=random.choice(operarios),
                    estado=random.choice(['planificada', 'en_curso', 'en_curso', 'completada', 'completada', 'pausada']),
                    fecha_inicio=timezone.now().date() - timedelta(days=random.randint(0, 365)),
                    metros_cubicos=random.uniform(100, 10000),
                    hectareas=random.uniform(5, 200),
                    observaciones="Generada automáticamente por seed_db",
                    activo=True
                )
                faenas.append(f)
                if i % 20 == 0: self.stdout.write(f'Faena creada: {f.nombre}')

        # 4. Crear Mantenciones (100)
        tipos_mantencion = ['preventiva', 'correctiva', 'emergencia', 'revision']
        
        if vehiculos:
            for i in range(100):
                vehiculo = random.choice(vehiculos)
                mecanico = random.choice([o for o in operarios if o.rol == 'mecanico']) if any(o.rol == 'mecanico' for o in operarios) else None
                
                Mantencion.objects.create(
                    vehiculo=vehiculo,
                    tipo=random.choice(tipos_mantencion),
                    estado=random.choice(['programada', 'en_proceso', 'completada', 'completada']),
                    descripcion=f'Mantención {random.choice(tipos_mantencion)} generada automáticamente',
                    fecha_programada=timezone.now().date() + timedelta(days=random.randint(-60, 60)),
                    fecha_realizada=timezone.now().date() if random.random() > 0.3 else None,
                    mecanico=mecanico,
                    costo=random.randint(50000, 2000000),
                    horas_vehiculo=vehiculo.horas_uso
                )
                if i % 20 == 0: self.stdout.write(f'Mantención creada para: {vehiculo.patente}')

        # 5. Crear Registros de Incidentes (50)
        tipos_incidente = ['accidente', 'incidente', 'casi_accidente', 'condicion_insegura']
        gravedades = ['leve', 'leve', 'moderado', 'grave', 'critico']

        if faenas:
            for i in range(50):
                faena = random.choice(faenas)
                RegistroIncidente.objects.create(
                    faena=faena,
                    tipo=random.choice(tipos_incidente),
                    gravedad=random.choice(gravedades),
                    descripcion='Incidente simulado generado por script de carga masiva',
                    fecha_incidente=timezone.now() - timedelta(days=random.randint(0, 100)),
                    operario_involucrado=faena.operario,
                    vehiculo_involucrado=faena.vehiculo,
                    reportado_por='Sistema Automático',
                    medidas_tomadas='Se aplicó protocolo de seguridad estándar.'
                )
                if i % 10 == 0: self.stdout.write(f'Incidente registrado en: {faena.nombre}')

        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada MASIVAMENTE con éxito!'))
