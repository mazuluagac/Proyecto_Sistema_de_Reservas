# Comunicación con Gateway - Microservicio de Notificaciones

## Configuración

Tu microservicio está configurado para comunicarse con el gateway usando:
- **Gateway URL**: `http://localhost:8000`
- **API Key**: `MiSuperLlaveUltraSecreta_z1127`
- **Nombre del Servicio**: `notifications`

## Headers Requeridos

Para cualquier comunicación con el gateway, incluye estos headers:

```
X-API-Key: MiSuperLlaveUltraSecreta_z1127
Content-Type: application/json
X-Service: notifications
Timestamp: [ISO datetime]
```

## Endpoints Disponibles

### 1. Health Check
**Ruta**: `GET /health`
**Descripción**: Verifica si el servicio está disponible

**Respuesta**:
```json
{
  "status": "healthy",
  "service": "notifications",
  "version": "1.0.0",
  "timestamp": "2025-11-16T10:30:00.000000"
}
```

### 2. Registrar Servicio
**Ruta**: `POST /register`
**Requiere**: API Key válida (header `X-API-Key`)

**Respuesta**:
```json
{
  "mensaje": "Microservicio registrado exitosamente",
  "service_info": {
    "name": "notifications",
    "url": "http://localhost:5000/",
    "endpoints": [...]
  }
}
```

### 3. Obtener Información del Servicio
**Ruta**: `GET /get_service_info`
**Descripción**: Retorna información sobre los endpoints disponibles

### 4. Enviar Notificación de Reserva
**Ruta**: `POST /send_reservation_notification/<reservation_id>`
**Parámetros**: 
- `reservation_id` (URL path): ID de la reserva

**Funcionalidad**:
- Obtiene datos de la reserva desde la BD
- Obtiene email del usuario desde BD de auth
- Envía correo HTML formateado
- Notifica al gateway del evento

**Respuesta exitosa**:
```json
{
  "mensaje": "Notificación de reserva enviada exitosamente",
  "destinatario": "usuario@email.com",
  "estado_reserva": "confirmada"
}
```

### 5. Enviar Todas las Notificaciones
**Ruta**: `GET /send_all_reservation_notifications`
**Descripción**: Envía notificaciones de todas las reservas pendientes

### 6. Notificación de Cambio de Estado
**Ruta**: `POST /notify_reservation_status/<reservation_id>`
**Requiere**: API Key válida
**Cuerpo JSON**:
```json
{
  "status": "confirmada"
}
```

## Funciones Internas

### `call_gateway_service(service_name, endpoint, method='GET', data=None, params=None)`

Realiza llamadas a otros microservicios a través del gateway.

**Ejemplo**:
```python
# Llamar al servicio de reservas
result = call_gateway_service(
    'reservation',
    '/reservas/1',
    method='GET'
)

# Llamar al servicio de usuarios
user_data = call_gateway_service(
    'users',
    '/users/5',
    method='GET'
)

# Enviar datos a otro servicio
response = call_gateway_service(
    'auth',
    '/validate',
    method='POST',
    data={'email': 'user@email.com'}
)
```

### `notify_gateway(event_type, data)`

Notifica al gateway sobre eventos importantes.

**Ejemplo**:
```python
notify_gateway('email_sent', {
    'reservation_id': 1,
    'user_id': 5,
    'recipient': 'user@email.com',
    'status': 'confirmada'
})
```

## Flujo de Comunicación

### Envío de Notificación (Flujo Normal)

```
1. Gateway recibe solicitud POST a /send_reservation_notification/1
   ↓
2. Microservicio verifica API Key
   ↓
3. Obtiene datos de reserva de BD local
   ↓
4. Obtiene email del usuario de BD local
   ↓
5. Genera correo HTML
   ↓
6. Envía correo mediante SMTP
   ↓
7. Notifica al gateway del evento
   ↓
8. Retorna respuesta de éxito
```

### Llamada a Otro Microservicio

```
1. Este microservicio llama a call_gateway_service()
   ↓
2. Construye URL al gateway
   ↓
3. Incluye API Key en headers
   ↓
4. Gateway enruta la solicitud al servicio correcto
   ↓
5. El otro servicio procesa la solicitud
   ↓
6. Gateway retorna respuesta
```

## Ejemplos de Uso

### Desde Python (dentro del microservicio)

```python
# Obtener información de una reserva desde otro microservicio
reservation_data = call_gateway_service(
    'reservation',
    '/reservas/1',
    method='GET'
)

if reservation_data:
    print(f"Reserva encontrada: {reservation_data}")
else:
    print("Error al obtener la reserva")
```

### Desde cURL (cliente externo)

```bash
# Health check
curl -X GET http://localhost:5000/health

# Enviar notificación
curl -X POST http://localhost:5000/send_reservation_notification/1 \
  -H "X-API-Key: MiSuperLlaveUltraSecreta_z1127"

# Registrar servicio
curl -X POST http://localhost:5000/register \
  -H "X-API-Key: MiSuperLlaveUltraSecreta_z1127"

# Obtener info del servicio
curl -X GET http://localhost:5000/get_service_info

# Notificar cambio de estado
curl -X POST http://localhost:5000/notify_reservation_status/1 \
  -H "X-API-Key: MiSuperLlaveUltraSecreta_z1127" \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmada"}'
```

## Seguridad

⚠️ **Importante**: 
- La API Key `MiSuperLlaveUltraSecreta_z1127` debe ser la misma en todos los microservicios
- Para producción, usa variables de entorno (`.env`) en lugar de hardcodear la API Key
- Todos los endpoints que requieren autenticación validan la API Key mediante el decorador `@validate_api_key`

## Integración con el Gateway

El gateway es responsable de:
1. Validar las API Keys
2. Enrutar las solicitudes al microservicio correcto
3. Mantener un registro de todos los servicios activos
4. Recopilar eventos de todos los servicios
5. Manejar reintentos en caso de error

Tu microservicio solo necesita:
1. Incluir la API Key en los headers
2. Llamar a los endpoints del gateway
3. Esperar las respuestas
