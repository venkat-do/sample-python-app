#!/usr/bin/env python
"""
Simple Django application entry point.
Uses Django's WSGI application directly to avoid path issues.
"""
import os
import sys
from pathlib import Path

# Add the Django project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'sampleproject'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleproject.settings')

# Import Django utilities
import django
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

def run_migrations():
    """Run database migrations"""
    print("Running database migrations...")
    original_cwd = os.getcwd()
    try:
        os.chdir(BASE_DIR / 'sampleproject')
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    finally:
        os.chdir(original_cwd)

def run_server():
    """Run the Django server using simple HTTP server"""
    from wsgiref import simple_server

    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'

    print(f"Starting Django server on {host}:{port}...")

    # Get the WSGI application
    application = get_wsgi_application()

    # Create and run the server
    server = simple_server.make_server(host, port, application)
    print(f"Django development server is running at http://{host}:{port}/")
    print("Quit the server with CONTROL-C.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Django server...")
        server.shutdown()

if __name__ == '__main__':
    # Setup Django
    django.setup()

    # Run migrations
    run_migrations()

    # Start the server
    run_server()
