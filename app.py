#!/usr/bin/env python
"""
Production entry point for Django application.
This file maintains compatibility with the existing benchmark configuration
while providing high-concurrency Django backend.
"""
import os
import sys
from pathlib import Path

# Add the Django project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'sampleproject'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleproject.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

def run_server():
    """Run the Django development server or production server based on environment"""
    port = int(os.environ.get('PORT', 8000))

    # Check if we should use Gunicorn for production
    if os.environ.get('USE_GUNICORN', 'true').lower() == 'true':
        # Use Gunicorn for high concurrency in production
        import subprocess
        cmd = [
            'gunicorn',
            '--bind', f'0.0.0.0:{port}',
            '--workers', str(os.environ.get('WORKERS', 4)),
            '--worker-class', 'sync',
            '--worker-connections', '1000',
            '--max-requests', '1000',
            '--max-requests-jitter', '100',
            '--timeout', '30',
            '--keepalive', '2',
            '--preload',
            'sampleproject.wsgi:application'
        ]

        # Change to the Django project directory
        os.chdir(BASE_DIR / 'sampleproject')

        print(f"Starting Django with Gunicorn on port {port} with high concurrency support...")
        subprocess.run(cmd)
    else:
        # Use Django development server (not recommended for production)
        print(f"Starting Django development server on port {port}...")
        os.chdir(BASE_DIR / 'sampleproject')
        execute_from_command_line([
            'manage.py', 'runserver', f'0.0.0.0:{port}'
        ])

if __name__ == '__main__':
    # Ensure Django is properly configured
    import django
    django.setup()

    # Run database migrations (creates tables if needed)
    print("Running database migrations...")
    os.chdir(BASE_DIR / 'sampleproject')
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])

    # Start the server
    run_server()
