from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import pymysql
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)

# ==========================================
# 1. CONFIGURACIÓN DE SEGURIDAD (GATEWAY)
# ==========================================
# Esta llave debe coincidir con la del docker-compose.yml
API_KEY = os.getenv('API_KEY', 'xK7mP9nQ2wR5tY8uI1oL4jH6gS3aZ0bVcX8zL2kJ5hG')
MICROSERVICE_NAME = 'notifications'

def validate_api_key(f):
    """
    Decorador para validar que la petición venga del Gateway
    usando la API Key compartida.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # El Gateway envía la llave en el header 'X-API-Key'
        request_key = request.headers.get('X-API-Key')
        
        if not request_key or request_key != API_KEY:
            return jsonify({
                'error': 'Acceso no autorizado: API Key inválida',
                'service': MICROSERVICE_NAME
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# 2. CONFIGURACIÓN DEL CORREO (INTACTO)
# ==========================================
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'pruebasopsmz@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'fnop mcib fknp vjhb')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'pruebasopsmz@gmail.com')
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

# ==========================================
# 3. CONFIGURACIÓN BASE DE DATOS (INTACTO)
# ==========================================
DB_CONFIG_AUTH = {
    'host': os.getenv('AUTH_DB_HOST', 'auth-db'),
    'user': os.getenv('AUTH_DB_USER', 'root'),
    'password': os.getenv('AUTH_DB_PASSWORD', 'secret'),
    'database': os.getenv('AUTH_DB_NAME', 'auth_db'),
    'port': int(os.getenv('AUTH_DB_PORT', '3306')),
    'charset': 'utf8mb4'
}

DB_CONFIG_RESERVATION = {
    'host': os.getenv('RESERVATION_DB_HOST', 'reservation-db'),
    'user': os.getenv('RESERVATION_DB_USER', 'root'),
    'password': os.getenv('RESERVATION_DB_PASSWORD', 'secret'),
    'database': os.getenv('RESERVATION_DB_NAME', 'reservation_db'),
    'port': int(os.getenv('RESERVATION_DB_PORT', '3306')),
    'charset': 'utf8mb4'
}

def get_db_connection(database='reservation'):
    try:
        if database == 'auth':
            return pymysql.connect(**DB_CONFIG_AUTH)
        else:
            return pymysql.connect(**DB_CONFIG_RESERVATION)
    except Exception as e:
        print(f"Error de conexión a BD {database}: {e}")
        return None

# ==========================================
# 4. CORREO FUNCIONES AUXILIARES
# ==========================================

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
                <p style='margin: 8px 0 0 0; color: #1b5e20;'>Estamos emocionados de tenerte con nosotros.</p>
            </div>
            <table style='border-collapse: collapse; margin: 16px 0; width: 100%;'>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de inicio:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_inicio}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de fin:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_fin}</td></tr>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Descripción:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{descripcion}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Estado:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd; color: #4caf50; font-weight: bold;'>{estado.upper()}</td></tr>
            </table>
            <p>Equipo de Reservas</p>
        </body>
        </html>
        """
    
    elif estado.lower() == 'pendiente':
        return f"""
        <html>
        <body style='font-family: Arial, sans-serif; color: #222;'>
            <h2 style='color: #1976d2;'>¡Hola {nombre_usuario}!</h2>
            <div style='background-color: #fff3e0; padding: 16px; border-radius: 8px; border-left: 4px solid #ff9800; margin: 16px 0;'>
                <h3 style='color: #ef6c00; margin: 0;'>⏳ Tu reserva está <b>PENDIENTE</b></h3>
            </div>
            <table style='border-collapse: collapse; margin: 16px 0; width: 100%;'>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de inicio:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_inicio}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de fin:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_fin}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Estado:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd; color: #ff9800; font-weight: bold;'>{estado.upper()}</td></tr>
            </table>
            <p>Equipo de Reservas</p>
        </body>
        </html>
        """
    
    else:
        return f"""
        <html>
        <body style='font-family: Arial, sans-serif; color: #222;'>
            <h2 style='color: #1976d2;'>¡Hola {nombre_usuario}!</h2>
            <div style='background-color: #ffebee; padding: 16px; border-radius: 8px; border-left: 4px solid #f44336; margin: 16px 0;'>
                <h3 style='color: #c62828; margin: 0;'>ℹ️ Actualización: <b>{estado.upper()}</b></h3>
            </div>
            <table style='border-collapse: collapse; margin: 16px 0; width: 100%;'>
                <tr style='background-color: #f5f5f5;'><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Fecha de inicio:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd;'>{fecha_inicio}</td></tr>
                <tr><td style='padding: 8px 12px; border: 1px solid #ddd;'><b>Estado:</b></td><td style='padding: 8px 12px; border: 1px solid #ddd; color: #f44336; font-weight: bold;'>{estado.upper()}</td></tr>
            </table>
            <p>Equipo de Reservas</p>
        </body>
        </html>
      """

# ==========================================
# 5. ENDPOINTS (RUTAS)
# ==========================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para el gateway (Vital para que funcione)"""
    return jsonify({
        'status': 'healthy',
        'service': MICROSERVICE_NAME,
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/simulate_notification/<int:reservation_id>', methods=['GET'])
def simulate_notification(reservation_id):
    """Simulación interna (No requiere auth del gateway para pruebas rápidas)"""
    try:
        with app.test_request_context():
            response = send_reservation_notification(reservation_id)
        return response
    except Exception as e:
        return jsonify({'mensaje': f'Error en la simulación: {str(e)}'}), 500
    
@app.route('/send_reservation_notification', methods=['GET'])
@validate_api_key  # <--- PROTEGIDO: Solo el Gateway puede llamar
def send_all_reservation_notifications():
    """Envía notificaciones de todas las reservas existentes."""
    conn_reservation = get_db_connection('reservation')
    if not conn_reservation:
        return jsonify({'mensaje': 'Error al conectar con la base de datos de reservas'}), 500

    enviados = []
    errores = []

    try:
        with conn_reservation.cursor() as cursor:
            sql = "SELECT id, usuario_id, nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado FROM reservas"
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

                    msg = Message(subject=asunto, recipients=[user_email], html=cuerpo_html, charset='utf-8')
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

@app.route('/send_reservation_notification/<int:reservation_id>', methods=['POST'])
@validate_api_key  # <--- PROTEGIDO: Solo el Gateway puede llamar
def send_reservation_notification(reservation_id):
    """Envía notificación de reserva basándose en el ID de reserva"""
    conn_reservation = get_db_connection('reservation')
    if not conn_reservation:
        return jsonify({'mensaje': 'Error al conectar con la base de datos de reservas'}), 500
    
    try:
        with conn_reservation.cursor() as cursor:
            sql = "SELECT usuario_id, nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado FROM reservas WHERE id = %s"
            cursor.execute(sql, (reservation_id,))
            reserva = cursor.fetchone()
            
            if not reserva:
                return jsonify({'mensaje': 'Reserva no encontrada'}), 404
            
            usuario_id, nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado = reserva
            
    except Exception as e:
        return jsonify({'mensaje': f'Error al obtener información de la reserva: {str(e)}'}), 500
    finally:
        conn_reservation.close()
    
    user_email = get_user_email(usuario_id)
    if not user_email:
        return jsonify({'mensaje': 'No se pudo obtener el email del usuario'}), 404
    
    try:
        asunto = f"Notificación de Reserva - Estado: {estado}"
        cuerpo_html = generar_cuerpo_html_por_estado(nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado)
        msg = Message(subject=asunto, recipients=[user_email], html=cuerpo_html, charset='utf-8')
        mail.send(msg)
        
        return jsonify({
            'mensaje': 'Notificación de reserva enviada exitosamente',
            'destinatario': user_email,
            'estado_reserva': estado
        }), 200
        
    except Exception as e:
        return jsonify({'mensaje': f'Error al enviar la notificación: {str(e)}'}), 500

@app.route('/get_user_email/<int:user_id>', methods=['GET'])
@validate_api_key  # <--- PROTEGIDO
def get_user_email_endpoint(user_id):
    """Endpoint para obtener el email de un usuario específico"""
    email = get_user_email(user_id)
    if email:
        return jsonify({'user_id': user_id, 'email': email}), 200
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# ==========================================
# 6. EJECUCIÓN LOCAL
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)