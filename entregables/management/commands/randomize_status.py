from django.core.management.base import BaseCommand
from entregables.models import Vehiculo, Operario, Faena, Mantencion, RegistroIncidente
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Aleatorizar TODOS los campos de la base de datos para pruebas exhaustivas'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando aleatorización COMPLETA de datos...')

        # Datos de prueba
        marcas = ['Volvo', 'Mercedes-Benz', 'Caterpillar', 'John Deere', 'Komatsu', 'Scania', 'MAN', 'Tigercat']
        nombres = ['Juan', 'Pedro', 'Luis', 'Carlos', 'Ana', 'Maria', 'Jose', 'Miguel', 'Roberto', 'Diego']
        apellidos = ['Perez', 'Gonzalez', 'Rodriguez', 'Lopez', 'Martinez', 'Sanchez', 'Fernandez']
        ubicaciones = ['Sector Los Pinos', 'Fundo El Roble', 'Predio San José', 'Lote 45', 'Cerro Alto']
        
        # 1. Aleatorizar Vehículos
        vehiculos = list(Vehiculo.objects.all())
        for v in vehiculos:
            v.tipo = random.choice([x[0] for x in Vehiculo.TIPOS])
            v.marca = random.choice(marcas)
            v.modelo = f'Modelo-{random.randint(100, 999)}'
            v.año = random.randint(1995, 2024)
            v.estado = random.choice([x[0] for x in Vehiculo.ESTADOS])
            
            # Lógica para forzar mantención en ~20% de los casos
            if random.random() < 0.2:
                v.horas_uso = random.randint(1, 40) * 500
            else:
                v.horas_uso = random.randint(1, 40) * 500
                
            v.capacidad_carga = random.uniform(5.0, 30.0)
            v.fecha_adquisicion = timezone.now().date() - timedelta(days=random.randint(0, 5000))
            
            # Fecha de creación posterior a adquisición
            dias_despues = random.randint(0, 30)
            fecha_registro = v.fecha_adquisicion + timedelta(days=dias_despues)
            hora = random.randint(8, 18)
            minuto = random.randint(0, 59)
            v.fecha_creacion = timezone.make_aware(
                timezone.datetime.combine(fecha_registro, timezone.datetime.min.time().replace(hour=hora, minute=minuto))
            )
            v.observaciones = f"Obs aleatoria {random.randint(1, 100)}"
            v.activo = random.random() > 0.1  # 90% activo
            v.save()
        self.stdout.write(f'Aleatorizados {len(vehiculos)} vehículos.')

        # 2. Aleatorizar Operarios
        operarios = list(Operario.objects.all())
        for o in operarios:
            o.nombre = f'{random.choice(nombres)} {random.choice(apellidos)}'
            o.rol = random.choice([x[0] for x in Operario.ROLES])
            o.licencia = random.choice(['A1', 'A2', 'A4', 'D'])
            o.telefono = f'+569{random.randint(10000000, 99999999)}'
            o.fecha_ingreso = timezone.now().date() - timedelta(days=random.randint(0, 3000))
            o.activo = random.random() > 0.1  # 90% activo
            o.save()
        self.stdout.write(f'Aleatorizados {len(operarios)} operarios.')

        # 3. Aleatorizar Faenas
        faenas = list(Faena.objects.all())
        for f in faenas:
            f.nombre = f'Faena {random.choice(["Norte", "Sur", "Este", "Oeste"])} {random.randint(1, 999)}'
            f.tipo = random.choice([x[0] for x in Faena.TIPOS])
            f.ubicacion = random.choice(ubicaciones)
            if vehiculos: f.vehiculo = random.choice(vehiculos)
            if operarios: f.operario = random.choice(operarios)
            f.estado = random.choice([x[0] for x in Faena.ESTADOS])
            f.fecha_inicio = timezone.now().date() - timedelta(days=random.randint(0, 365))
            f.fecha_termino = f.fecha_inicio + timedelta(days=random.randint(1, 90)) if random.choice([True, False]) else None
            f.metros_cubicos = random.uniform(50, 5000)
            f.hectareas = random.uniform(1, 100)
            f.observaciones = f"Faena random {random.randint(1, 100)}"
            f.activo = random.random() > 0.1  # 90% activo
            f.save()
        self.stdout.write(f'Aleatorizadas {len(faenas)} faenas.')

        # 4. Aleatorizar Mantenciones
        mantenciones = Mantencion.objects.all()
        mecanicos = [o for o in operarios if o.rol == 'mecanico']
        for m in mantenciones:
            if vehiculos: m.vehiculo = random.choice(vehiculos)
            m.tipo = random.choice([x[0] for x in Mantencion.TIPOS])
            m.estado = random.choice([x[0] for x in Mantencion.ESTADOS])
            m.descripcion = f"Mantención random {random.randint(1, 1000)}"
            m.fecha_programada = timezone.now().date() + timedelta(days=random.randint(-30, 30))
            m.fecha_realizada = m.fecha_programada if m.estado == 'completada' else None
            if mecanicos: m.mecanico = random.choice(mecanicos)
            m.costo = random.randint(10000, 1000000)
            m.repuestos_utilizados = f"Repuesto-{random.randint(1, 50)}"
            m.horas_vehiculo = random.randint(100, 10000)
            m.save()
        self.stdout.write(f'Aleatorizadas {mantenciones.count()} mantenciones.')

        # 5. Aleatorizar Incidentes
        incidentes = RegistroIncidente.objects.all()
        for i in incidentes:
            if faenas: i.faena = random.choice(faenas)
            i.tipo = random.choice([x[0] for x in RegistroIncidente.TIPOS])
            i.gravedad = random.choice([x[0] for x in RegistroIncidente.GRAVEDAD])
            i.descripcion = f"Incidente random {random.randint(1, 100)}"
            i.fecha_incidente = timezone.now() - timedelta(days=random.randint(0, 60))
            if operarios: i.operario_involucrado = random.choice(operarios)
            if vehiculos: i.vehiculo_involucrado = random.choice(vehiculos)
            i.medidas_tomadas = "Protocolo estándar aplicado"
            i.reportado_por = f"Supervisor {random.randint(1, 10)}"
            i.save()
        self.stdout.write(f'Aleatorizados {incidentes.count()} incidentes.')

        self.stdout.write(self.style.SUCCESS('¡Base de datos TOTALMENTE aleatorizada!'))
