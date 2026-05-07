from django.core.management.commands.runserver import Command as RunserverCommand
import threading
import webbrowser
import time


class Command(RunserverCommand):
    help = 'Starts a lightweight Web server for development and optionally opens the browser.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--open',
            action='store_true',
            dest='open',
            help='Open the default web browser to the server URL after starting.'
        )

    def handle(self, *args, **options):
        open_browser = options.pop('open', False)

        # Determine the address/port the server will bind to.
        addrport = None
        if args and args[0]:
            addrport = args[0]
        else:
            # Fallback to default used by RunserverCommand
            addrport = '127.0.0.1:8000'

        # Normalize host/port
        if ':' in addrport:
            host, port = addrport.split(':', 1)
        else:
            host = '127.0.0.1'
            port = addrport

        if host == '0.0.0.0':
            # If binding to all interfaces, open localhost in browser.
            host_for_open = '127.0.0.1'
        else:
            host_for_open = host

        url = f'http://{host_for_open}:{port}/'

        if open_browser:
            def _open():
                # Wait a short moment for the server to start accepting connections.
                time.sleep(1.0)
                try:
                    webbrowser.open(url)
                except Exception:
                    # Non-fatal: opening the browser is a convenience.
                    pass

            t = threading.Thread(target=_open, daemon=True)
            t.start()

        # Call the original runserver handler (this will block until server stops)
        return super().handle(*args, **options)
