from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import os
import psutil
import time
from .storage import storage

@require_http_methods(["GET"])
def home(request):
    """Main endpoint showing application info and available endpoints"""
    return JsonResponse({
        'message': 'Hello from Python Django!',
        'runtime': 'Python',
        'framework': 'Django',
        'status': 'running',
        'server': 'High Performance Django Server',
        'database': 'In-Memory Storage (No DB)',
        'endpoints': {
            'root': '/',
            'health': '/health',
            'users': '/api/users',
            'stats': '/api/stats',
            'echo': '/api/echo',
            'items': '/api/items'
        }
    })

@require_http_methods(["GET"])
def health(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'sample-django-service',
        'framework': 'Django',
        'storage': 'in-memory',
        'database': 'none',
        'timestamp': time.time()
    })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def users(request):
    """Users endpoint with in-memory storage"""
    if request.method == 'GET':
        users_data = storage.list('users')
        return JsonResponse(users_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = storage.create('users', data)
            user = storage.get('users', user_id)
            return JsonResponse(user, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

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
            'server_type': 'High Performance Django Server',
            'storage': {
                'type': 'in-memory',
                'users_count': storage.count('users'),
                'items_count': storage.count('items')
            }
        })
    except Exception as e:
        # Fallback stats if psutil is not available
        return JsonResponse({
            'server': 'sample-django-app',
            'framework': 'Django',
            'pid': os.getpid(),
            'timestamp': time.time(),
            'server_type': 'High Performance Django Server',
            'storage': {
                'type': 'in-memory',
                'users_count': storage.count('users'),
                'items_count': storage.count('items')
            },
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
                data = dict(request.POST)

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

# New endpoint for generic items CRUD operations
@csrf_exempt
@require_http_methods(["GET", "POST"])
def items_view(request):
    """Items endpoint for CRUD operations"""
    if request.method == "GET":
        items = storage.list("items")
        return JsonResponse({"items": items, "count": len(items)})

    elif request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            item_id = storage.create("items", data)
            item = storage.get("items", item_id)
            return JsonResponse(item, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def item_detail_view(request, item_id):
    """Individual item operations"""
    if request.method == "GET":
        item = storage.get("items", item_id)
        if item:
            return JsonResponse(item)
        return JsonResponse({"error": "Item not found"}, status=404)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body.decode('utf-8'))
            if storage.update("items", item_id, data):
                item = storage.get("items", item_id)
                return JsonResponse(item)
            return JsonResponse({"error": "Item not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    elif request.method == "DELETE":
        if storage.delete("items", item_id):
            return JsonResponse({"message": "Item deleted"})
        return JsonResponse({"error": "Item not found"}, status=404)
