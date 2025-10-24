from django.core.management.base import BaseCommand
from datetime import date
from typing import Any, List, Dict
import random
import calendar
import uuid

from equipos.models import Equipo


class Command(BaseCommand):
    help = 'Cargar datos de ejemplo para la app equipos (aleatorios desde un dictado)'

    def add_arguments(self, parser: Any):
        parser.add_argument('--count', type=int, default=5,
                            help='Número de equipos de ejemplo a crear')

    def random_date(self, start_year: int = 2015, end_year: int = date.today().year) -> date:
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        last_day = calendar.monthrange(year, month)[1]
        day = random.randint(1, last_day)
        return date(year, month, day)

    def handle(self, **options: Any) -> None:
        count = options.get('count', 5)

        choices: Dict[str, List[str]] = {
            'nombres': [
                'Proyector Epson X1', 'Notebook Lenovo V14', 'Impresora HP LaserJet',
                'Router Cisco 2901', 'Proyector BenQ P30', 'Switch Netgear GS108',
                'Monitor Samsung 24"', 'Tablet Samsung Tab A', 'Servidor Dell PowerEdge'
            ],
            'categorias': ['Proyector', 'Notebook', 'Impresora', 'Router', 'Switch', 'Monitor', 'Tablet', 'Servidor'],
            'estados': ['Operativo', 'En reparación', 'Dado de baja', 'En mantenimiento'],
            'ubicaciones': ['Sala 201', 'Laboratorio 3', 'Sala 101', 'Bodega', 'Sala 202', 'Oficina Central']
        }

        created = 0
        for _ in range(count):
            nombre_base = random.choice(choices['nombres'])
            categoria = random.choice(choices['categorias'])
            estado = random.choice(choices['estados'])
            ubicacion = random.choice(choices['ubicaciones'])
            fecha_ingreso = self.random_date(2015, date.today().year)

            # Añadir sufijo corto para reducir colisiones en get_or_create
            suffix = uuid.uuid4().hex[:6]
            nombre = f"{nombre_base} ({suffix})"

            _, was_created = Equipo.objects.get_or_create(
                nombre=nombre,
                categoria=categoria,
                ubicacion=ubicacion,
                defaults={
                    'estado': estado,
                    'fecha_ingreso': fecha_ingreso,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Se crearon {created} equipo(s) de ejemplo.'))
