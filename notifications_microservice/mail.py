from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import pymysql
import requests
from functools import wraps
from datetime import datetime

app = Flask(__name__)

# ===== CONFIGURACIÓN DEL GATEWAY =====
GATEWAY_URL = 'http://localhost:8000'  # URL del gateway
API_KEY = 'MiSuperLlaveUltraSecreta_z1127'  # Tu API Key
MICROSERVICE_NAME = 'notifications'  # Nombre de este microservicio

# ===== FUNCIONES DE AUTENTICACIÓN CON GATEWAY =====
def validate_api_key(f):
    """Decorador para validar API_KEY en las solicitudes internas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != API_KEY:
            return jsonify({'error': 'API Key inválida o no proporcionada'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_gateway_headers():
    """Retorna los headers necesarios para comunicarse con el gateway"""
    return {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json',
        'X-Service': MICROSERVICE_NAME,
        'Timestamp': datetime.now().isoformat()
    }

def call_gateway_service(service_name, endpoint, method='GET', data=None, params=None):
    """
    Realiza una llamada a otro microservicio a través del gateway
    
    Args:
        service_name: Nombre del servicio (ej: 'reservation', 'auth', 'users')
        endpoint: Ruta del endpoint del servicio (ej: '/get_user/1')
        method: Método HTTP (GET, POST, PUT, DELETE)
        data: Datos a enviar en POST/PUT
        params: Parámetros de query
    
    Returns:
        Response del servicio o None si hay error
    """
    try:
        url = f"{GATEWAY_URL}/{service_name}{endpoint}"
        headers = get_gateway_headers()
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, params=params, timeout=10)
        else:
            return None
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con {service_name}: {str(e)}")
        return None

def notify_gateway(event_type, data):
    """
    Notifica al gateway sobre eventos importantes del microservicio
    
    Args:
        event_type: Tipo de evento (ej: 'email_sent', 'email_failed')
        data: Datos del evento
    """
    try:
        event_data = {
            'service': MICROSERVICE_NAME,
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        url = f"{GATEWAY_URL}/events"
        headers = get_gateway_headers()
        requests.post(url, json=event_data, headers=headers, timeout=5)
    except Exception as e:
        print(f"Error al notificar al gateway: {str(e)}")

# Configuración del correo electrónico
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'pruebasopsmz@gmail.com'
app.config['MAIL_PASSWORD'] = 'fnop mcib fknp vjhb'
app.config['MAIL_DEFAULT_SENDER'] = 'pruebasopsmz@gmail.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = False

# Configuración de las bases de datos
DB_CONFIG_AUTH = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'auth_db',  # Base de datos de autenticación
    'charset': 'utf8mb4'
}

DB_CONFIG_RESERVATION = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'reservation_db',  # Base de datos de reservas
    'charset': 'utf8mb4'
}

def get_db_connection(database='reservation'):
    """
    Obtiene conexión a la base de datos especificada
    Opciones: 'reservation' o 'auth'
    """
    try:
        if database == 'auth':
            return pymysql.connect(**DB_CONFIG_AUTH)
        else:
            return pymysql.connect(**DB_CONFIG_RESERVATION)
    except Exception as e:
        print(f"Error de conexión a BD {database}: {e}")
        return None

mail = Mail(app)

def get_user_email(user_id):
    """Obtiene el email del usuario desde la base de datos de autenticación"""
    conn = get_db_connection('auth')
    if not conn:
        return None
    
    try:
        with conn.cursor() as cursor:
            sql = "SELECT email FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error al obtener email del usuario: {e}")
        return None
    finally:
        conn.close()

def generar_cuerpo_html_por_estado(nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado):
    """Genera el cuerpo HTML del correo según el estado de la reserva"""
    
    if estado.lower() == 'confirmada':
        return f"""
        <html>
        <body style='font-family: Arial, sans-serif; color: #222;'>
            <h2 style='color: #1976d2;'>¡Hola {nombre_usuario}!</h2>
            
            <div style='background-color: #e8f5e9; padding: 16px; border-radius: 8px; border-left: 4px solid #4caf50; margin: 16px 0;'>
                <h3 style='color: #2e7d32; margin: 0;'>🎉 ¡Tu reserva ha sido <b>CONFIRMADA</b>!</h3>
                <p style='margin: 8px 0 0 0; color: #1b5e20;'>Estamos emocionados de tenerte con nosotros. Tu reserva está lista y confirmada.</p>
            </div>
            
            <table style='border-collapse: collapse; margin: 16px 0; width: 100%;'>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de inicio:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_inicio}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de fin:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_fin}</td></tr>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Descripción:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{descripcion}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Estado:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd; color: #4caf50; font-weight: bold;'>{estado.upper()}</td></tr>
            </table>
            
            <div style='background-color: #e3f2fd; padding: 12px; border-radius: 6px; margin: 16px 0;'>
                <p style='margin: 0; color: #1565c0;'><b>📌 Recuerda:</b> Llega puntual a tu reserva. Si necesitas hacer algún cambio, contáctanos con anticipación.</p>
            </div>
            
            <p>Si tienes dudas o necesitas modificar tu reserva, responde a este correo o contáctanos a través de la plataforma.</p>
            
            <p style='margin-top: 24px;'>¡Estamos ansiosos por atenderte!<br><span style='color: #1976d2; font-weight: bold;'>Equipo de Reservas</span></p>
        </body>
        </html>
        """
    
    elif estado.lower() == 'pendiente':
        return f"""
        <html>
        <body style='font-family: Arial, sans-serif; color: #222;'>
            <h2 style='color: #1976d2;'>¡Hola {nombre_usuario}!</h2>
            
            <div style='background-color: #fff3e0; padding: 16px; border-radius: 8px; border-left: 4px solid #ff9800; margin: 16px 0;'>
                <h3 style='color: #ef6c00; margin: 0;'>⏳ Tu reserva está <b>PENDIENTE</b> de confirmación</h3>
                <p style='margin: 8px 0 0 0; color: #e65100;'>Estamos procesando tu solicitud. Te notificaremos tan pronto como sea confirmada.</p>
            </div>
            
            <table style='border-collapse: collapse; margin: 16px 0; width: 100%;'>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de inicio:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_inicio}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de fin:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_fin}</td></tr>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Descripción:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{descripcion}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Estado:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd; color: #ff9800; font-weight: bold;'>{estado.upper()}</td></tr>
            </table>
            
            <div style='background-color: #fff8e1; padding: 12px; border-radius: 6px; margin: 16px 0;'>
                <p style='margin: 0; color: #ff8f00;'><b>💡 Importante:</b> Tu reserva no está confirmada aún. Por favor espera nuestra confirmación final.</p>
            </div>
            
            <p>Si tienes alguna pregunta urgente sobre tu reserva pendiente, no dudes en contactarnos.</p>
            
            <p style='margin-top: 24px;'>¡Gracias por tu paciencia!<br><span style='color: #1976d2; font-weight: bold;'>Equipo de Reservas</span></p>
        </body>
        </html>
        """
    
    else:  # Para otros estados (cancelada, rechazada, etc.)
        return f"""
        <html>
        <body style='font-family: Arial, sans-serif; color: #222;'>
            <h2 style='color: #1976d2;'>¡Hola {nombre_usuario}!</h2>
            
            <div style='background-color: #ffebee; padding: 16px; border-radius: 8px; border-left: 4px solid #f44336; margin: 16px 0;'>
                <h3 style='color: #c62828; margin: 0;'>ℹ️ Actualización de tu reserva</h3>
                <p style='margin: 8px 0 0 0; color: #b71c1c;'>El estado de tu reserva ha cambiado a: <b>{estado.upper()}</b></p>
            </div>
            
            <table style='border-collapse: collapse; margin: 16px 0; width: 100%;'>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de inicio:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_inicio}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de fin:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_fin}</td></tr>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Descripción:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{descripcion}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Estado:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd; color: #f44336; font-weight: bold;'>{estado.upper()}</td></tr>
            </table>
            
            <p>Si tienes dudas sobre este cambio de estado, por favor contáctanos para más información.</p>
            
            <p style='margin-top: 24px;'>Atentamente,<br><span style='color: #1976d2; font-weight: bold;'>Equipo de Reservas</span></p>
        </body>
        </html>

      """
    
@app.route('/simulate_notification/<int:reservation_id>', methods=['GET'])
def simulate_notification(reservation_id):
    """
    Simula el envío de una notificación de reserva (solo para pruebas de rendimiento).
    Llama internamente al mismo proceso de envío de notificación.
    """
    try:
        # Llama directamente la función principal que ya tienes
        with app.test_request_context():
            response = send_reservation_notification(reservation_id)
        return response
    except Exception as e:
        return jsonify({'mensaje': f'Error en la simulación: {str(e)}'}), 500
    
@app.route('/send_reservation_notification', methods=['GET'])
def send_all_reservation_notifications():
    """
    Envía notificaciones de todas las reservas existentes.
    Ideal para pruebas de rendimiento.
    """
    conn_reservation = get_db_connection('reservation')
    if not conn_reservation:
        return jsonify({'mensaje': 'Error al conectar con la base de datos de reservas'}), 500

    enviados = []
    errores = []

    try:
        with conn_reservation.cursor() as cursor:
            sql = """
            SELECT id, usuario_id, nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado
            FROM reservas
            """
            cursor.execute(sql)
            reservas = cursor.fetchall()

            if not reservas:
                return jsonify({'mensaje': 'No hay reservas registradas'}), 200

            for reserva in reservas:
                try:
                    id_reserva, usuario_id, nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado = reserva
                    user_email = get_user_email(usuario_id)

                    if not user_email:
                        errores.append({'id_reserva': id_reserva, 'error': 'Usuario sin email'})
                        continue

                    asunto = f"Notificación de Reserva - Estado: {estado}"
                    cuerpo_html = generar_cuerpo_html_por_estado(
                        nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado
                    )

                    msg = Message(
                        subject=asunto,
                        recipients=[user_email],
                        html=cuerpo_html,
                        charset='utf-8'
                    )
                    mail.send(msg)
                    enviados.append({'id_reserva': id_reserva, 'email': user_email, 'estado': estado})
                except Exception as e:
                    errores.append({'id_reserva': id_reserva, 'error': str(e)})

        return jsonify({
            'mensaje': f'Notificaciones enviadas: {len(enviados)}',
            'exitosos': enviados,
            'errores': errores
        }), 200

    except Exception as e:
        return jsonify({'mensaje': f'Error general: {str(e)}'}), 500
    finally:
        conn_reservation.close()

'''
@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    destinatario = data.get('destinatario')
    asunto = data.get('asunto')
    cuerpo = data.get('cuerpo')

    if not all([destinatario, asunto, cuerpo]):
        return jsonify({'mensaje': 'Faltan campos por llenar'}), 400

    try:
        msg = Message(
            subject=asunto,
            recipients=[destinatario],
            body=cuerpo,
            charset='utf-8'
        )
        mail.send(msg)
        return jsonify({'mensaje': 'Correo enviado exitosamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error al enviar el correo: {str(e)}'}), 500
'''

@app.route('/send_reservation_notification/<int:reservation_id>', methods=['POST'])
def send_reservation_notification(reservation_id):
    """Envía notificación de reserva basándose en el ID de reserva"""
    # Obtener información de la reserva
    conn_reservation = get_db_connection('reservation')
    if not conn_reservation:
        return jsonify({'mensaje': 'Error al conectar con la base de datos de reservas'}), 500
    
    try:
        with conn_reservation.cursor() as cursor:
            sql = """
            SELECT usuario_id, nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado 
            FROM reservas 
            WHERE id = %s
            """
            cursor.execute(sql, (reservation_id,))
            reserva = cursor.fetchone()
            
            if not reserva:
                return jsonify({'mensaje': 'Reserva no encontrada'}), 404
            
            usuario_id, nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado = reserva
            
    except Exception as e:
        return jsonify({'mensaje': f'Error al obtener información de la reserva: {str(e)}'}), 500
    finally:
        conn_reservation.close()
    
    # Obtener el email del usuario desde la base de datos de autenticación
    user_email = get_user_email(usuario_id)
    
    if not user_email:
        return jsonify({'mensaje': 'No se pudo obtener el email del usuario'}), 404
    
    # Preparar y enviar el correo
    try:
        asunto = f"Notificación de Reserva - Estado: {estado}"
        
        # Generar el cuerpo HTML según el estado
        cuerpo_html = generar_cuerpo_html_por_estado(
            nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado
        )
        
        msg = Message(
            subject=asunto,
            recipients=[user_email],
            html=cuerpo_html,
            charset='utf-8'
        )
        mail.send(msg)
        
        return jsonify({
            'mensaje': 'Notificación de reserva enviada exitosamente',
            'destinatario': user_email,
            'estado_reserva': estado
        }), 200
        
    except Exception as e:
        return jsonify({'mensaje': f'Error al enviar la notificación: {str(e)}'}), 500

@app.route('/get_user_email/<int:user_id>', methods=['GET'])
def get_user_email_endpoint(user_id):
    """Endpoint para obtener el email de un usuario específico"""
    email = get_user_email(user_id)
    
    if email:
        return jsonify({'user_id': user_id, 'email': email}), 200
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# ===== ENDPOINTS PARA COMUNICACIÓN CON GATEWAY =====
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para el gateway"""
    return jsonify({
        'status': 'healthy',
        'service': MICROSERVICE_NAME,
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/register', methods=['POST'])
@validate_api_key
def register_service():
    """Registra este microservicio con el gateway"""
    try:
        service_info = {
            'name': MICROSERVICE_NAME,
            'url': request.host_url,
            'endpoints': [
                '/send_reservation_notification/<reservation_id>',
                '/send_all_reservation_notifications',
                '/get_user_email/<user_id>',
                '/health'
            ],
            'timestamp': datetime.now().isoformat()
        }
        return jsonify({
            'mensaje': 'Microservicio registrado exitosamente',
            'service_info': service_info
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_service_info', methods=['GET'])
def get_service_info():
    """Retorna información del microservicio"""
    return jsonify({
        'name': MICROSERVICE_NAME,
        'description': 'Microservicio de notificaciones por email',
        'endpoints': {
            'send_notification': {
                'path': '/send_reservation_notification/<reservation_id>',
                'method': 'POST',
                'description': 'Envía notificación de reserva'
            },
            'get_all_notifications': {
                'path': '/send_all_reservation_notifications',
                'method': 'GET',
                'description': 'Envía notificaciones de todas las reservas'
            },
            'health': {
                'path': '/health',
                'method': 'GET',
                'description': 'Verifica el estado del servicio'
            }
        }
    }), 200

@app.route('/notify_reservation_status/<int:reservation_id>', methods=['POST'])
@validate_api_key
def notify_reservation_status(reservation_id):
    """
    Endpoint que recibe notificaciones del gateway sobre cambios de estado en reservas
    Se puede llamar desde otros microservicios a través del gateway
    """
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'Status es requerido'}), 400
        
        # Obtener información de la reserva y enviar notificación
        result = send_reservation_notification(reservation_id)
        
        return jsonify({
            'mensaje': f'Notificación enviada para reserva {reservation_id}',
            'nuevo_status': new_status
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)