#!/usr/bin/env python
"""
High-performance Django application entry point.
Uses multi-threaded server to handle high RPS without external dependencies.
"""
import os
import sys
from pathlib import Path
import threading
from wsgiref import simple_server
from socketserver import ThreadingMixIn

# Add the Django project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'sampleproject'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleproject.settings')

# Import Django utilities
import django
from django.core.wsgi import get_wsgi_application

class ThreadedWSGIServer(ThreadingMixIn, simple_server.WSGIServer):
    """Multi-threaded WSGI server for handling concurrent requests"""
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, *args, **kwargs):
        # Set a reasonable thread pool size
        self.request_queue_size = 100  # Allow up to 100 queued connections
        super().__init__(*args, **kwargs)

def run_server():
    """Run the Django server using multi-threaded HTTP server"""
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'

    print(f"Starting high-performance Django server on {host}:{port}...")
    print("Server optimizations:")
    print("- No database dependencies (in-memory storage)")
    print("- Multi-threaded request handling")
    print("- Minimal middleware stack")
    print("- Disabled logging for performance")

    # Get the WSGI application
    application = get_wsgi_application()

    # Create multi-threaded server
    server = simple_server.make_server(
        host, port, application,
        server_class=ThreadedWSGIServer
    )

    print(f"High-performance Django server running at http://{host}:{port}/")
    print("Available endpoints:")
    print("  GET  /              - Home page with server info")
    print("  GET  /health        - Health check")
    print("  GET  /api/users     - List users")
    print("  POST /api/users     - Create user")
    print("  GET  /api/stats     - Server statistics")
    print("  GET  /api/items     - List items")
    print("  POST /api/items     - Create item")
    print("  GET  /api/echo      - Echo endpoint")
    print("  POST /api/echo      - Echo with data")
    print("Ready to handle high RPS! Press CTRL+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down high-performance Django server...")
        server.shutdown()

if __name__ == '__main__':
    # Setup Django
    django.setup()

    # Start the high-performance server
    run_server()
