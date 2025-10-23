from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import os
import psutil
import time

@require_http_methods(["GET"])
def home(request):
    """Main endpoint showing application info and available endpoints"""
    return JsonResponse({
        'message': 'Hello from Python Django!',
        'runtime': 'Python',
        'framework': 'Django',
        'status': 'running',
        'server': 'Django Development Server',
        'endpoints': {
            'root': '/',
            'health': '/health',
            'users': '/api/users',
            'stats': '/api/stats',
            'echo': '/api/echo'
        }
    })

@require_http_methods(["GET"])
def health(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'sample-django-service',
        'framework': 'Django',
        'timestamp': time.time()
    })

@require_http_methods(["GET"])
def users(request):
    """Sample users endpoint"""
    users_data = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'},
        {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com'}
    ]
    return JsonResponse(users_data, safe=False)

@require_http_methods(["GET"])
def stats(request):
    """Server statistics endpoint"""
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()

        return JsonResponse({
            'server': 'sample-django-app',
            'framework': 'Django',
            'pid': os.getpid(),
            'memory': {
                'rss': memory_info.rss,
                'vms': memory_info.vms
            },
            'cpu_percent': process.cpu_percent(),
            'create_time': process.create_time(),
            'timestamp': time.time(),
            'server_type': 'Django Development Server'
        })
    except Exception as e:
        # Fallback stats if psutil is not available
        return JsonResponse({
            'server': 'sample-django-app',
            'framework': 'Django',
            'pid': os.getpid(),
            'timestamp': time.time(),
            'server_type': 'Django Development Server',
            'note': 'Basic stats - psutil not available'
        })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def echo(request):
    """Echo endpoint that returns request data"""
    if request.method == 'GET':
        return JsonResponse({
            'message': 'Echo endpoint - send POST request with JSON data',
            'method': 'GET',
            'timestamp': time.time()
        })

    if request.method == 'POST':
        try:
            # Try to parse JSON data
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST.dict()

            return JsonResponse({
                'message': 'Echo response',
                'receivedData': data,
                'method': 'POST',
                'content_type': request.content_type,
                'headers': dict(request.headers),
                'timestamp': time.time()
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON',
                'message': 'Could not parse request body',
                'timestamp': time.time()
            }, status=400)
