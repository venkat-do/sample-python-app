#!/usr/bin/env python
"""
Django WSGI entry point for high-performance load testing.
Use gunicorn for production-grade concurrency and performance.
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
from django.core.wsgi import get_wsgi_application

def main():
    django.setup()
    application = get_wsgi_application()
    return application

# For gunicorn, expose 'application' as module-level variable
application = main()

if __name__ == '__main__':
    print("This script is intended to be run with gunicorn:")
    print("  gunicorn app:application --workers 4 --threads 8 --bind 0.0.0.0:8000")
    print("Or use your preferred gunicorn settings for load testing.")
