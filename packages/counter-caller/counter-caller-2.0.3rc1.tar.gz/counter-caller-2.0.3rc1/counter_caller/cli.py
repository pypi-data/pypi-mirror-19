import click
from counter_caller.app import app, sock

@click.command()
@click.option('bind', '-b', '--bind', default='0.0.0.0:5000', type=str, help='Host/port to bind to (default: 0.0.0.0:5000)')
def run(bind):
    host, port = bind.split(':', 2)
    sock.run(app, host=host, port=int(port))
