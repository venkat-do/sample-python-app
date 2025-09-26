# Sample Python Flask Service

A simple Python Flask application for benchmarking deployment performance.

## Features

- Simple HTTP endpoints
- Health check endpoint
- JSON responses
- Environment-based port configuration

## Endpoints

- `GET /` - Returns service information
- `GET /health` - Health check endpoint

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

The service will run on port 8000 by default, or use the PORT environment variable.

## Deployment

This app is designed to work with DigitalOcean App Platform and other cloud providers that support Python applications.
