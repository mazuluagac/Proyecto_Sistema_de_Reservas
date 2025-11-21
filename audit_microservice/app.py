from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from flask.json.provider import DefaultJSONProvider
from functools import wraps  # Import necesario para el decorador
import os
import json

# -----------------------------------------------------------
# Configuración base del microservicio
# -----------------------------------------------------------
app = Flask(__name__)

# Configuración de Seguridad (Gateway)
API_KEY = os.getenv('API_KEY', 'xK7mP9nQ2wR5tY8uI1oL4jH6gS3aZ0bVcX8zL2kJ5hG')
MICROSERVICE_NAME = 'audit'

# Configuración de Mongo
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "audit_db")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[MONGO_DB]
    # Verificamos conexión inicial
    client.server_info()
    auditoria_collection = db["audit_logs"] # Cambié nombre a uno más estándar, puedes usar el que quieras
except Exception as e:
    print(f"Error conectando a MongoDB: {e}")
    auditoria_collection = None

# -----------------------------------------------------------
# Middleware de Seguridad
# -----------------------------------------------------------
def validate_api_key(f):
    """
    Valida que la petición venga del Gateway usando la API Key compartida.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_key = request.headers.get('X-API-Key')
        
        if not request_key or request_key != API_KEY:
            return jsonify({
                'error': 'Acceso no autorizado',
                'message': 'API Key inválida o faltante'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------------------------------------
# Serializador para ObjectId de Mongo
# -----------------------------------------------------------
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

app.json = CustomJSONProvider(app)

# -----------------------------------------------------------
#  Endpoint para health check (Público para el Gateway)
# -----------------------------------------------------------
@app.route('/health', methods=['GET'])
def health_check():
    # Verificamos si Mongo responde
    db_status = 'healthy'
    if auditoria_collection is None:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy', 
        'db_status': db_status,
        'service': MICROSERVICE_NAME
    }), 200

# -----------------------------------------------------------
# 1️ Endpoint para registrar eventos de auditoría
# -----------------------------------------------------------
@app.route('/audit', methods=['POST'])
@validate_api_key  # <--- PROTEGIDO
def log_audit():
    if auditoria_collection is None:
        return jsonify({"error": "No hay conexión con la base de datos"}), 500

    data = request.get_json()

    if not data or 'action' not in data:
        return jsonify({"error": "Faltan campos requeridos (action)"}), 400

    evento = {
        "action": data['action'],
        "user_id": data.get('user_id', 'system'), # Default a 'system' si no viene
        "fecha": datetime.now().isoformat(),
        "ip": request.remote_addr, # Agregamos IP de origen
        "details": data.get('details', {})
    }

    try:
        result = auditoria_collection.insert_one(evento)
        evento["_id"] = str(result.inserted_id)
        return jsonify({"message": "Evento registrado", "event": evento}), 201
    except Exception as e:
        return jsonify({"error": f"Error al guardar en Mongo: {str(e)}"}), 500

# -----------------------------------------------------------
# 2️ Endpoint para listar eventos
# -----------------------------------------------------------
@app.route('/audit', methods=['GET'])
@validate_api_key  # <--- PROTEGIDO
def get_audit_logs():
    if auditoria_collection is None:
        return jsonify({"error": "No hay conexión con la base de datos"}), 500
        
    try:
        # Limite opcional para no traer millones de registros
        limit = int(request.args.get('limit', 100))
        eventos = list(auditoria_collection.find().sort("fecha", -1).limit(limit))
        return jsonify({"total": len(eventos), "events": eventos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------
# 3️ Endpoint raíz
# -----------------------------------------------------------
@app.route('/')
def index():
    return jsonify({"service": "Audit Service", "version": "1.0"}), 200

# -----------------------------------------------------------
# 4️ Ejecutar servidor
# -----------------------------------------------------------
if __name__ == '__main__':
    # Importante: host='0.0.0.0' para que Docker lo exponga correctamente
    app.run(host='0.0.0.0', port=5004, debug=False)