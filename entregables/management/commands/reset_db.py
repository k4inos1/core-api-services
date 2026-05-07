from django.core.management.base import BaseCommand
from django.core.management import call_command
from entregables.models import Vehiculo, Operario, Faena  # Asegúrate de importar tus modelos

class Command(BaseCommand):
    help = 'Reinicia la base de datos eliminando las tablas de la aplicación y volviéndolas a crear.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--seed',
            action='store_true',
            help='Poblar la base de datos después de reiniciar',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando reinicio de la base de datos...'))
        
        # 1. Eliminar tablas (revertir migraciones)
        self.stdout.write('Eliminando tablas de la aplicación...')
        call_command('migrate', 'entregables', 'zero')
        
        # 2. Volver a crear tablas (aplicar migraciones)
        self.stdout.write('Recreando tablas...')
        call_command('migrate')
        
        self.stdout.write(self.style.SUCCESS('¡Base de datos reiniciada correctamente!'))

        # 3. Poblar si se solicita
        if options['seed']:
            self.stdout.write('Poblando base de datos...')
            call_command('seed_db')
            call_command('randomize_status')
            self.stdout.write(self.style.SUCCESS('¡Base de datos poblada y aleatorizada!'))

        # Establecer estado activo por defecto para todos los modelos
        Vehiculo.objects.update(activo=True)
        Operario.objects.update(activo=True)
        Faena.objects.update(activo=True)
