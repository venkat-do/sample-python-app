# Sample Django Web Application

A simple Django web application for benchmarking and testing purposes, using Django's built-in development server.

## Features

- **Django Framework**: Clean, maintainable Python web framework
- **Built-in Server**: Uses Django's development server for simplicity
- **Health Check**: Built-in health monitoring endpoint
- **REST API**: Clean API endpoints with Django views
- **JSON Responses**: Structured JSON responses for all endpoints
- **Database Ready**: SQLite database with Django ORM
- **Static Files**: WhiteNoise for efficient static file serving

## Architecture

- **Framework**: Django 4.2.7 (Python web framework)
- **Server**: Django's built-in development server
- **Database**: SQLite with Django ORM
- **Static Files**: WhiteNoise middleware

## Endpoints

- `GET /` - Welcome message with application info and endpoint list
- `GET /health` - Health check endpoint
- `GET /api/users` - Sample users data
- `GET /api/stats` - Server statistics and performance metrics
- `POST /api/echo` - Echo back request data
- `GET /api/echo` - Echo endpoint information

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

The server will start on port 8000 (or PORT environment variable).

## Environment Variables

- `PORT` - Server port (default: 8000)
- `DEBUG` - Enable Django debug mode (default: false)
- `SECRET_KEY` - Django secret key for production

## Deployment

This application is designed for deployment on:
- DigitalOcean App Platform
- Heroku
- AWS ECS/Fargate
- Google Cloud Run
- Any container platform supporting Python/Django

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

## Development

The application uses Django's built-in development server, which automatically:
- Handles database migrations on startup
- Serves static files
- Provides detailed error pages in debug mode
- Auto-reloads on code changes (in development mode)
