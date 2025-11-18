from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from flask.json.provider import DefaultJSONProvider
import json

# -----------------------------------------------------------
# Configuración base del microservicio
# -----------------------------------------------------------
app = Flask(__name__)

# Conexión a MongoDB (base de datos local)
client = MongoClient("mongodb://localhost:27017")
db = client["microservicios"]
auditoria_collection = db["audit_db_test"]

# -----------------------------------------------------------
# Serializador para ObjectId de Mongo
# -----------------------------------------------------------
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

app.json = CustomJSONProvider(app)

# -----------------------------------------------------------
# 1️ Endpoint para registrar eventos de auditoría
# -----------------------------------------------------------
@app.route('/audit', methods=['POST'])
def log_audit():
    """
    Registra una acción realizada por el sistema o un usuario.
    Por ejemplo: crear_usuario, login, logout, actualizar_perfil, etc.
    """
    data = request.get_json()

    # Validar que los campos mínimos existan
    if not data or 'action' not in data:
        return jsonify({"error": "Faltan campos requeridos (action)"}), 400

    # Crear evento de auditoría
    evento = {
        "action": data['action'],
        "user_id": data['user_id'],
        "fecha": datetime.now().isoformat(),
        "details": data.get('details', {})
    }

    # Guardar evento en MongoDB
    result = auditoria_collection.insert_one(evento)
    evento["_id"] = str(result.inserted_id)

    return jsonify({"message": "Evento de auditoría registrado", "event": evento}), 201

# -----------------------------------------------------------
# 2️ Endpoint para listar todos los eventos registrados
# -----------------------------------------------------------
@app.route('/audit', methods=['GET'])
def get_audit_logs():

    # Devuelve todos los eventos registrados en la base de datos.
    eventos = list(auditoria_collection.find())
    return jsonify({"total": len(eventos), "events": eventos}), 200
# -----------------------------------------------------------
# 3️ Endpoint raíz (para verificar estado del servicio)
# -----------------------------------------------------------
@app.route('/')
def index():
    return "Microservicio de Auditoría en ejecución", 200

# -----------------------------------------------------------
# 4️ Ejecutar servidor
# -----------------------------------------------------------
if __name__ == '__main__':
    app.run(port=5004, debug=True)
