# Sample Django Web Application

A high-performance Django web application for benchmarking and testing purposes, designed for superior concurrency compared to Flask-based alternatives.

## Features

- **High Concurrency**: Django with Gunicorn WSGI server for production-grade performance
- **Multiple Workers**: Configurable worker processes for handling concurrent requests
- **Health Check**: Built-in health monitoring endpoint
- **REST API**: Clean API endpoints with Django views
- **JSON Responses**: Structured JSON responses for all endpoints
- **Production Ready**: Optimized for deployment with proper WSGI configuration
- **Database Ready**: SQLite database with Django ORM (easily switchable to PostgreSQL/MySQL)

## Architecture

- **Framework**: Django 4.2.7 (Python web framework)
- **WSGI Server**: Gunicorn with configurable workers
- **Static Files**: WhiteNoise for efficient static file serving
- **Database**: SQLite (development) / PostgreSQL (production)
- **Concurrency**: Multi-worker process model with sync workers

## Endpoints

- `GET /` - Welcome message with application info and endpoint list
- `GET /health` - Health check endpoint
- `GET /api/users` - Sample users data
- `GET /api/stats` - Server statistics and performance metrics
- `POST /api/echo` - Echo back request data
- `GET /api/echo` - Echo endpoint information

## Running Locally

### Development Mode
```bash
pip install -r requirements.txt
python app.py
```

### Production Mode (with Gunicorn)
```bash
pip install -r requirements.txt
export USE_GUNICORN=true
export WORKERS=4
python app.py
```

The server will start on port 8000 (or PORT environment variable).

## Environment Variables

- `PORT` - Server port (default: 8000)
- `USE_GUNICORN` - Use Gunicorn for production (default: true)
- `WORKERS` - Number of Gunicorn worker processes (default: 4)
- `DEBUG` - Enable Django debug mode (default: false)
- `SECRET_KEY` - Django secret key for production

## Performance Configuration

The application is optimized for high concurrency with:

- **Gunicorn WSGI Server**: Production-grade application server
- **Multiple Workers**: 4 worker processes by default (configurable)
- **Connection Pooling**: Database connection reuse and pooling
- **Static File Optimization**: WhiteNoise for efficient static file serving
- **Request Handling**: Async-capable Django views with proper HTTP method decorators

## Deployment

This application is designed for high-performance deployment on:
- DigitalOcean App Platform
- Heroku
- AWS ECS/Fargate
- Google Cloud Run
- Any container platform supporting WSGI

## Concurrency Advantages over Flask

- **Better Multi-threading**: Django's thread-safe design
- **Production WSGI**: Built-in Gunicorn configuration
- **Worker Process Model**: Multiple processes for true parallelism
- **Database Connection Pooling**: Efficient database connection management
- **Middleware Stack**: Optimized request/response processing

## API Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Users
```bash
curl http://localhost:8000/api/users
```

### Server Stats
```bash
curl http://localhost:8000/api/stats
```

### Echo Data
```bash
curl -X POST http://localhost:8000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Django!"}'
```
