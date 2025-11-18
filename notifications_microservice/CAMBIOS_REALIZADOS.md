# Resumen de Cambios - Integración con Gateway

## Cambios Realizados

### 1. **Actualización del archivo `mail.py`**

Se agregaron las siguientes funcionalidades:

#### Configuración del Gateway
```python
GATEWAY_URL = 'http://localhost:8000'
API_KEY = 'MiSuperLlaveUltraSecreta_z1127'
MICROSERVICE_NAME = 'notifications'
```

#### Funciones Principales

1. **`validate_api_key(f)`** - Decorador
   - Valida que el header `X-API-Key` sea correcto
   - Protege endpoints internos

2. **`get_gateway_headers()`** - Función utilitaria
   - Retorna headers necesarios para comunicarse con el gateway
   - Incluye timestamp automático

3. **`call_gateway_service(service_name, endpoint, method='GET', data=None, params=None)`** - Función principal
   - Realiza llamadas a otros microservicios a través del gateway
   - Soporta GET, POST, PUT, DELETE
   - Manejo de errores integrado

4. **`notify_gateway(event_type, data)`** - Función de eventos
   - Notifica al gateway sobre eventos importantes
   - Tipos: 'email_sent', 'email_failed', etc.

#### Nuevos Endpoints

| Endpoint | Método | Descripción | Requiere API Key |
|----------|--------|-------------|------------------|
| `/health` | GET | Verifica estado del servicio | No |
| `/register` | POST | Registra el servicio con el gateway | Sí |
| `/get_service_info` | GET | Retorna información del servicio | No |
| `/notify_reservation_status/<id>` | POST | Recibe notificación de cambio de estado | Sí |

#### Actualización de Endpoints Existentes

- **`/send_reservation_notification/<id>`**: Ahora notifica al gateway con `notify_gateway()`
- Incluye validación de API Key opcional

### 2. **Actualización de `requirements.txt`**

Se agregaron las dependencias necesarias:
```
requests          # Para hacer llamadas HTTP al gateway
Flask-Mail        # Confirmación de dependencia
```

### 3. **Nuevos Archivos Creados**

#### `GATEWAY_COMMUNICATION.md`
- Documentación completa de la integración
- Ejemplos de uso con cURL
- Descripción de todos los endpoints
- Flujos de comunicación

#### `GATEWAY_EXAMPLES.py`
- 10 ejemplos prácticos de uso
- Ejemplos de llamadas a otros microservicios
- Manejo de errores
- Flujos completos

#### `.env.example`
- Plantilla de configuración
- Variables de entorno necesarias
- Puede ser renombrado a `.env` y completado

## Cómo Usar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno (opcional)
```bash
cp .env.example .env
# Editar .env si es necesario
```

### 3. Ejecutar el microservicio
```bash
python mail.py
```

### 4. Probar la comunicación

#### Health check
```bash
curl -X GET http://localhost:5000/health
```

#### Registrar con el gateway
```bash
curl -X POST http://localhost:5000/register \
  -H "X-API-Key: MiSuperLlaveUltraSecreta_z1127"
```

#### Enviar notificación
```bash
curl -X POST http://localhost:5000/send_reservation_notification/1 \
  -H "X-API-Key: MiSuperLlaveUltraSecreta_z1127"
```

## Flujo de Funcionamiento

```
Solicitud Externa
        ↓
     Gateway
        ↓
   Validar API Key
        ↓
   Enrutar a microservicio
        ↓
  Microservicio (notifications)
        ↓
  Procesar solicitud
        ↓
  Opcionalmente: Llamar a otros microservicios via gateway
        ↓
  Notificar eventos al gateway
        ↓
   Retornar respuesta
```

## Características de Seguridad

✅ **API Key Validation** - Todos los endpoints internos requieren API Key
✅ **Headers Automáticos** - Timestamp incluido en cada solicitud
✅ **Service Identification** - El gateway sabe de qué servicio viene la solicitud
✅ **Timeout Protection** - Timeouts configurados en llamadas al gateway

## Ejemplo de Integración Completa

```python
# En uno de tus endpoints
@app.route('/send_notification/<int:reservation_id>', methods=['POST'])
@validate_api_key
def send_notification(reservation_id):
    # 1. Obtener datos de otro microservicio
    reservation = call_gateway_service(
        'reservation',
        f'/reservas/{reservation_id}'
    )
    
    if not reservation:
        return jsonify({'error': 'Reserva no encontrada'}), 404
    
    # 2. Procesar (enviar correo)
    # ...
    
    # 3. Notificar al gateway
    notify_gateway('email_sent', {
        'reservation_id': reservation_id,
        'status': 'success'
    })
    
    return jsonify({'message': 'Notificado exitosamente'}), 200
```

## Próximos Pasos

1. ✅ Configurar el archivo `.env` con tus valores reales
2. ✅ Actualizar la URL del gateway si es diferente a `http://localhost:8000`
3. ✅ Implementar validación de API Key en otros microservicios
4. ✅ Configurar el gateway para enrutar solicitudes correctamente
5. ✅ Probar comunicación entre microservicios

## API Key Actual

**⚠️ IMPORTANTE**: Tu API Key es: `MiSuperLlaveUltraSecreta_z1127`

Esta debe ser la **MISMA** en todos los microservicios.

Para producción, considera:
- Usar variables de entorno
- Implementar rotación de keys
- Usar HTTPS en lugar de HTTP
- Implementar mecanismos de rate limiting
