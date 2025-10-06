from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["microservicios"]
auditoria_collection = db["audit_db"]

# -----------------------------------------------------------
# 1️⃣ Endpoint para registrar un evento de auditoría
# -----------------------------------------------------------

@app.route('/audit', methods=['POST'])
def log_audit():

    # Obtener datos del request
    data=request.get_json()

    # Validar que llegaron los datos necesarios
    if not data or 'action' not in data or 'user_id' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    #Crear el evento
    evento = {
        "action": data['action'],
        "user_id": data['user_id'],
        "fecha": datetime.now().isoformat(),
        "details": data.get('details', {})
    }

    # Guardar el evento en la base de datos
    auditoria_collection.insert_one(evento)

    return jsonify({"message": "Evento creado exitosamente", "event": evento}), 201

# -----------------------------------------------------------
# 2️⃣ Endpoint para obtener todos los eventos de auditoría
# -----------------------------------------------------------

@app.route('/audit', methods=['GET'])
def get_audit_logs():
    eventos = list(auditoria_collection.find({}, {'_id': 0}))
    return jsonify(
        {"total": len(eventos), "events": eventos}
    ), 200

# -----------------------------------------------------------
# 3️⃣ Endpoint para filtrar eventos por usuario  
# -----------------------------------------------------------

@app.route('/audit/buscar', methods=['GET'])
def buscar_audit_logs():
    action = request.args.get('action')
    user_id = request.args.get('user_id')

    query = {}
    if action:
        query['action'] = action
    if user_id:
        query['user_id'] = user_id

    resultados = list(auditoria_collection.find(query, {'_id': 0}))
    return jsonify(
        {"total": len(resultados), "events": resultados}
    ), 200

@app.route('/')
def index():
    return "Microservicio de Auditoría en ejecución ✅"

if __name__ == '__main__':
    app.run(port=5004,debug=True)