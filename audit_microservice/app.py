from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from flask.json.provider import DefaultJSONProvider
import os
import json

# -----------------------------------------------------------
# Configuración base del microservicio
# -----------------------------------------------------------
app = Flask(__name__)

# Leer variables del entorno enviadas desde docker-compose
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "audit_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# Nombre de la colección
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
    data = request.get_json()

    if not data or 'action' not in data:
        return jsonify({"error": "Faltan campos requeridos (action)"}), 400

    evento = {
        "action": data['action'],
        "user_id": data.get('user_id', None),   # ← evita errores si no viene
        "fecha": datetime.now().isoformat(),
        "details": data.get('details', {})
    }

    result = auditoria_collection.insert_one(evento)
    evento["_id"] = str(result.inserted_id)

    return jsonify({"message": "Evento de auditoría registrado", "event": evento}), 201

# -----------------------------------------------------------
# 2️ Endpoint para listar eventos
# -----------------------------------------------------------
@app.route('/audit', methods=['GET'])
def get_audit_logs():
    eventos = list(auditoria_collection.find())
    return jsonify({"total": len(eventos), "events": eventos}), 200

# -----------------------------------------------------------
# 3️ Endpoint raíz
# -----------------------------------------------------------
@app.route('/')
def index():
    return "Microservicio de Auditoría en ejecución", 200

# -----------------------------------------------------------
# 4️ Ejecutar servidor
# -----------------------------------------------------------
if __name__ == '__main__':
    app.run(port=5004, debug=True)
