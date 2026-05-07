from django.core.management.base import BaseCommand
from django.core.management import call_command
import threading
import webbrowser
import time


class Command(BaseCommand):
    help = 'Run the development server and optionally open the browser (--open).'

    def add_arguments(self, parser):
        # Minimal parsing: accept addrport as optional positional and a --open flag.
        parser.add_argument('addrport', nargs='?', help='Optional address:port')
        parser.add_argument('--open', action='store_true', dest='open', help='Open the default web browser to the server URL after starting.')

    def handle(self, *args, **options):
        open_browser = options.pop('open', False)
        addrport = options.pop('addrport', None)

        # Build url for browser
        if not addrport:
            host_for_open = '127.0.0.1'
            port = '8000'
        else:
            if ':' in addrport:
                host, port = addrport.split(':', 1)
            else:
                host = '127.0.0.1'
                port = addrport
            host_for_open = '127.0.0.1' if host == '0.0.0.0' else host

        url = f'http://{host_for_open}:{port}/'

        # Start a thread to open the browser after a short delay
        if open_browser:
            def _open():
                time.sleep(1.0)
                try:
                    webbrowser.open(url)
                except Exception:
                    pass

            threading.Thread(target=_open, daemon=True).start()

        # Call the built-in runserver command, forward only the addrport positional.
        if addrport:
            return call_command('runserver', addrport)
        else:
            return call_command('runserver')
