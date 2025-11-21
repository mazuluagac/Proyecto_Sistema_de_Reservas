import os
from django.http import JsonResponse

class GatewaySecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Leemos la API Key del entorno
        self.API_KEY = os.getenv('API_KEY')

    def __call__(self, request):
        # 1. Excepciones: Permitir health check y admin sin API Key
        # (Admin solo funciona si tienes rutas para ello en el gateway, pero es bueno dejarlo accesible internamente)
        if request.path == '/health' or request.path.startswith('/admin/'):
            return self.get_response(request)

        # 2. Obtener la llave del Header
        # Django transforma 'X-API-Key' a 'HTTP_X_API_KEY'
        request_key = request.META.get('HTTP_X_API_KEY')

        # 3. Validar
        if request_key != self.API_KEY:
            return JsonResponse({
                'error': 'Acceso denegado',
                'message': 'Petición no autorizada por el API Gateway',
                'service': 'reports-service'
            }, status=401)

        return self.get_response(request)