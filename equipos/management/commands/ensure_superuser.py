from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Ensure a superuser exists. Usage: manage.py ensure_superuser --username USER --email E --password P"

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True,
                            help='Username for the superuser')
        parser.add_argument('--email', required=True,
                            help='Email for the superuser')
        parser.add_argument('--password', required=False,
                            help='Password for the superuser (if omitted, will prompt)')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options.get('password')

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' already exists."))
            return

        if not password:
            from django.contrib.auth.management.commands.createsuperuser import getpass

            password = getpass.getpass()

        User.objects.create_superuser(
            username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(
            f"Superuser '{username}' created."))
