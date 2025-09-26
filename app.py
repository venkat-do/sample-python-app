from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return {
        'message': 'Hello from Python Flask!',
        'runtime': 'Python',
        'framework': 'Flask',
        'status': 'running',
        'health endpoint': '/health'
    }

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'sample-python-service'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
