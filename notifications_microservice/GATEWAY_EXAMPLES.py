"""
EJEMPLOS DE USO: Comunicación con Otros Microservicios a través del Gateway

Este archivo muestra ejemplos prácticos de cómo usar las funciones 
call_gateway_service() y notify_gateway() desde el microservicio de notificaciones.

API_KEY: MiSuperLlaveUltraSecreta_z1127
"""

# ============================================
# EJEMPLO 1: Obtener información de un usuario
# ============================================
def ejemplo_get_user_info():
    """
    Llama al microservicio de usuarios para obtener información
    """
    from mail import call_gateway_service
    
    user_id = 5
    
    # Hacer la llamada al servicio de usuarios a través del gateway
    user_data = call_gateway_service(
        service_name='users',
        endpoint=f'/users/{user_id}',
        method='GET'
    )
    
    if user_data:
        print(f"Datos del usuario: {user_data}")
        # Usar los datos obtenidos...
    else:
        print("Error al obtener datos del usuario")


# ============================================
# EJEMPLO 2: Obtener información de una reserva
# ============================================
def ejemplo_get_reservation_info():
    """
    Llama al microservicio de reservas para obtener información detallada
    """
    from mail import call_gateway_service
    
    reservation_id = 1
    
    # Hacer la llamada al servicio de reservas
    reservation_data = call_gateway_service(
        service_name='reservation',
        endpoint=f'/reservas/{reservation_id}',
        method='GET'
    )
    
    if reservation_data:
        print(f"Detalles de la reserva: {reservation_data}")
    else:
        print("Reserva no encontrada")


# ============================================
# EJEMPLO 3: Validar credenciales en Auth
# ============================================
def ejemplo_validate_auth():
    """
    Llama al microservicio de autenticación para validar credenciales
    """
    from mail import call_gateway_service
    
    auth_data = {
        'email': 'usuario@email.com',
        'password': 'password123'
    }
    
    # Hacer la llamada al servicio de auth
    validation_result = call_gateway_service(
        service_name='auth',
        endpoint='/validate',
        method='POST',
        data=auth_data
    )
    
    if validation_result and validation_result.get('valid'):
        print("Credenciales válidas")
    else:
        print("Credenciales inválidas")


# ============================================
# EJEMPLO 4: Crear una nuevar reserva
# ============================================
def ejemplo_create_reservation():
    """
    Llama al microservicio de reservas para crear una nueva reserva
    """
    from mail import call_gateway_service
    
    new_reservation = {
        'usuario_id': 5,
        'nombre_usuario': 'Juan Pérez',
        'fecha_inicio': '2025-12-01',
        'fecha_fin': '2025-12-05',
        'descripcion': 'Suite de lujo',
        'estado': 'pendiente'
    }
    
    # Hacer la llamada para crear la reserva
    response = call_gateway_service(
        service_name='reservation',
        endpoint='/reservas',
        method='POST',
        data=new_reservation
    )
    
    if response and response.get('id'):
        print(f"Reserva creada con ID: {response['id']}")
    else:
        print("Error al crear la reserva")


# ============================================
# EJEMPLO 5: Actualizar estado de reserva
# ============================================
def ejemplo_update_reservation_status():
    """
    Llama al microservicio de reservas para actualizar el estado
    """
    from mail import call_gateway_service
    
    reservation_id = 1
    update_data = {
        'estado': 'confirmada',
        'fecha_confirmacion': '2025-11-16'
    }
    
    # Hacer la llamada para actualizar
    response = call_gateway_service(
        service_name='reservation',
        endpoint=f'/reservas/{reservation_id}',
        method='PUT',
        data=update_data
    )
    
    if response:
        print(f"Reserva actualizada: {response}")
    else:
        print("Error al actualizar la reserva")


# ============================================
# EJEMPLO 6: Notificar eventos al Gateway
# ============================================
def ejemplo_notify_events():
    """
    Notifica al gateway sobre eventos importantes
    """
    from mail import notify_gateway
    
    # Evento de correo enviado exitosamente
    notify_gateway(
        event_type='email_sent',
        data={
            'reservation_id': 1,
            'user_id': 5,
            'recipient': 'usuario@email.com',
            'status': 'confirmada',
            'timestamp': '2025-11-16T10:30:00'
        }
    )
    
    print("Evento notificado al gateway")


# ============================================
# EJEMPLO 7: Obtener lista de servicios disponibles
# ============================================
def ejemplo_get_available_services():
    """
    Obtiene la lista de todos los microservicios disponibles en el gateway
    """
    from mail import call_gateway_service
    
    # Esta llamada depende de la implementación del gateway
    services = call_gateway_service(
        service_name='gateway',
        endpoint='/services',
        method='GET'
    )
    
    if services:
        print(f"Servicios disponibles: {services}")
    else:
        print("No se pudo obtener la lista de servicios")


# ============================================
# EJEMPLO 8: Manejo de errores
# ============================================
def ejemplo_manejo_errores():
    """
    Ejemplo de cómo manejar errores en la comunicación con el gateway
    """
    from mail import call_gateway_service
    
    try:
        result = call_gateway_service(
            service_name='users',
            endpoint='/users/999',  # Usuario que probablemente no existe
            method='GET'
        )
        
        if result is None:
            print("El servicio no está disponible o hubo un error de conexión")
        elif 'error' in result:
            print(f"Error del servidor: {result['error']}")
        else:
            print(f"Resultado exitoso: {result}")
            
    except Exception as e:
        print(f"Excepción no manejada: {str(e)}")


# ============================================
# EJEMPLO 9: Flujo completo - Procesar notificación
# ============================================
def ejemplo_flujo_completo():
    """
    Ejemplo completo que integra varias operaciones:
    1. Obtener datos de reserva
    2. Obtener datos de usuario
    3. Enviar notificación
    4. Notificar eventos
    """
    from mail import call_gateway_service, notify_gateway, get_user_email
    
    reservation_id = 1
    
    # Paso 1: Obtener info de la reserva
    reservation = call_gateway_service(
        service_name='reservation',
        endpoint=f'/reservas/{reservation_id}',
        method='GET'
    )
    
    if not reservation:
        print("No se pudo obtener la reserva")
        return
    
    # Paso 2: Obtener datos del usuario
    user_id = reservation.get('usuario_id')
    user = call_gateway_service(
        service_name='users',
        endpoint=f'/users/{user_id}',
        method='GET'
    )
    
    if not user:
        print("No se pudo obtener los datos del usuario")
        return
    
    # Paso 3: Obtener email del usuario (desde BD local o gateway)
    user_email = get_user_email(user_id)
    
    if not user_email:
        print("No se pudo obtener el email del usuario")
        return
    
    # Paso 4: En este punto, enviarías el email (con mail.send())
    print(f"Enviando notificación a {user_email}")
    
    # Paso 5: Notificar al gateway del evento
    notify_gateway(
        event_type='email_sent',
        data={
            'reservation_id': reservation_id,
            'user_id': user_id,
            'recipient': user_email,
            'status': reservation.get('estado')
        }
    )
    
    print("Notificación completada")


# ============================================
# EJEMPLO 10: Headers personalizados
# ============================================
def ejemplo_custom_headers():
    """
    Muestra los headers que se envían automáticamente
    """
    from mail import get_gateway_headers
    
    headers = get_gateway_headers()
    
    print("Headers enviados al gateway:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    
    """
    Salida esperada:
    Headers enviados al gateway:
      X-API-Key: MiSuperLlaveUltraSecreta_z1127
      Content-Type: application/json
      X-Service: notifications
      Timestamp: 2025-11-16T10:30:00.123456
    """


# ============================================
# USO EN ENDPOINTS DE FLASK
# ============================================
"""
Ejemplo de cómo usar estas funciones dentro de un endpoint Flask:

from flask import Flask, request, jsonify
from mail import call_gateway_service, notify_gateway

@app.route('/process_reservation/<int:reservation_id>', methods=['POST'])
def process_reservation(reservation_id):
    # Obtener datos del gateway
    reservation = call_gateway_service(
        'reservation',
        f'/reservas/{reservation_id}'
    )
    
    if not reservation:
        return jsonify({'error': 'Reserva no encontrada'}), 404
    
    try:
        # Procesar la reserva...
        
        # Notificar al gateway del resultado
        notify_gateway('reservation_processed', {
            'reservation_id': reservation_id,
            'status': 'success'
        })
        
        return jsonify({'message': 'Procesado exitosamente'}), 200
        
    except Exception as e:
        notify_gateway('reservation_failed', {
            'reservation_id': reservation_id,
            'error': str(e)
        })
        return jsonify({'error': str(e)}), 500
"""

if __name__ == '__main__':
    print("Este es un archivo de referencia con ejemplos de uso.")
    print("Los ejemplos están documentados pero no se ejecutan automáticamente.")
