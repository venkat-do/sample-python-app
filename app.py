#!/usr/bin/env python
"""
Simple Django application entry point.
Uses Django's built-in development server for simplicity.
"""
import os
import sys
from pathlib import Path

# Add the Django project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'sampleproject'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleproject.settings')

# Import Django management utilities
from django.core.management import execute_from_command_line

def run_server():
    """Run the Django development server"""
    port = int(os.environ.get('PORT', 8000))

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
