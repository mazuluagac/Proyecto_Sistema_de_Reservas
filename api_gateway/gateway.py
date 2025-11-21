from flask import Flask, request, jsonify, Response
import requests
import os
from datetime import datetime
from functools import wraps
import logging
from werkzeug.exceptions import HTTPException

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN DE SERVICIOS
# ==========================================

API_KEY = os.getenv('API_KEY', '')

SERVICES = {
    'auth': os.getenv('AUTH_SERVICE_URL', 'http://auth-service:8000'),
    'reservations': os.getenv('RESERVATION_SERVICE_URL', 'http://reservation-service:8002'),
    'notifications': os.getenv('NOTIFICATIONS_SERVICE_URL', 'http://notifications-service:5000'),
    'reports': os.getenv('REPORTS_SERVICE_URL', 'http://reports-service:8001'),
    'audit': os.getenv('AUDIT_SERVICE_URL', 'http://audit_service:5004')
}

PUBLIC_ROUTES = [
    '/api/auth/login',
    '/api/auth/register',
    '/health',
    '/api/health'
]

# ==========================================
# AUTENTICACIÓN
# ==========================================

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if any(request.path.startswith(route) for route in PUBLIC_ROUTES):
            return f(*args, **kwargs)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'success': False, 'message': 'Token no proporcionado'}), 401

        try:
            token_type, token = auth_header.split(' ')
            if token_type.lower() != 'bearer':
                raise ValueError()
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Formato inválido. Use: Bearer <token>'
            }), 401
        
        return f(*args, **kwargs)
    return wrapper

# ==========================================
# PROXY REQUEST
# ==========================================

def proxy_request(service_name, path='', method=None):
    service_url = SERVICES.get(service_name)

    if not service_url:
        return jsonify({'success': False, 'message': f'Servicio no encontrado: {service_name}'}), 404

    # Construir URL destino
    url = f"{service_url}{path}"

    method = method or request.method

    # Copiar headers excepto los conflictivos
    headers = {
        key: value for key, value in request.headers.items()
        if key.lower() not in ['host', 'connection', 'content-length']
    }

    headers['X-API-Key'] = API_KEY
    headers['X-Gateway'] = 'api-gateway'
    headers['X-Forwarded-For'] = request.remote_addr

    logger.info(f"Proxy → {method} {url}")

    try:
        data = request.get_json(silent=True)
        params = request.args

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params,
            timeout=30
        )

        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )

    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'message': 'Timeout al conectar con el servicio'}), 504

    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'message': 'No se pudo conectar con el servicio'}), 503

    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return jsonify({'success': False, 'message': 'Error interno del gateway'}), 500

# ==========================================
# HEALTH CHECK
# ==========================================

@app.route('/health', methods=['GET'])
def health_check():
    services_status = {}

    for name, base_url in SERVICES.items():
        try:
            response = requests.get(f"{base_url}/health", timeout=5, headers={'X-API-Key': API_KEY})
            services_status[name] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'url': base_url,
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            services_status[name] = {
                'status': 'unreachable',
                'url': base_url,
                'error': str(e)
            }

    return jsonify({
        'success': True,
        'service': 'api-gateway',
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'services': services_status
    })

# ==========================================
# PROXIES
# ==========================================

@app.route('/api/auth/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def auth_proxy(path):
    return proxy_request('auth', f'/api/{path}')

@app.route('/api/reservas', methods=['GET', 'POST'])
@app.route('/api/reservas/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@require_auth
def reservations_proxy(path=''):
    return proxy_request('reservations', f'/api/reservas/{path}' if path else '/api/reservas')

@app.route('/api/notifications/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@require_auth
def notifications_proxy(path):
    return proxy_request('notifications', f'/{path}')

@app.route('/api/reports/<path:path>', methods=['GET', 'POST'])
@require_auth
def reports_proxy(path):
    return proxy_request('reports', f'/api/{path}')

@app.route('/api/audit/<path:path>', methods=['GET', 'POST'])
@require_auth
def audit_proxy(path):
    return proxy_request('audit', f'/{path}')

# ==========================================
# INFO DEL GATEWAY
# ==========================================

@app.route('/gateway/info')
def gateway_info():
    return jsonify({
        'success': True,
        'gateway': 'API Gateway v1.0.0',
        'services': SERVICES,
        'public_routes': PUBLIC_ROUTES
    })

# ==========================================
# ERRORES
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Ruta no encontrada en el Gateway',
        'path': request.path
    }), 404

@app.errorhandler(Exception)
def global_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({'success': False, 'message': e.description}), e.code

    logger.error(f"Excepción global: {e}")
    return jsonify({'success': False, 'message': 'Error inesperado en el Gateway'}), 500

# ==========================================
# LOGGING
# ==========================================

@app.before_request
def log_before():
    logger.info(f"[REQ] {request.method} {request.path}")

@app.after_request
def log_after(response):
    logger.info(f"[RES] {response.status_code}")
    return response

@app.after_request
def cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
    return response

# ==========================================
# START
# ==========================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print("🚀 API GATEWAY listo")
    app.run(host='0.0.0.0', port=port, debug=False)
