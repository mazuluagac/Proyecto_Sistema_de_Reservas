# 🚀 API Gateway

Gateway centralizado para la arquitectura de microservicios del sistema de reservas. Actúa como punto de entrada único para todos los servicios backend, manejando enrutamiento, autenticación y comunicación entre servicios.

## ✨ Características

- **Enrutamiento Centralizado**: Punto de entrada único para todos los microservicios
- **Autenticación JWT**: Validación de tokens Bearer en rutas protegidas
- **Proxy Inteligente**: Reenvío transparente de peticiones HTTP
- **Health Checks**: Monitoreo del estado de todos los servicios
- **Manejo de Errores**: Respuestas consistentes ante fallos
- **CORS Habilitado**: Acceso desde clientes web
- **Logging Completo**: Registro de todas las peticiones y respuestas
- **Timeout y Retry**: Manejo robusto de conexiones
- **Producción Ready**: Optimizado con Gunicorn y workers múltiples

## 🏗 Arquitectura

```
Cliente → API Gateway (puerto 3000) → Microservicios (red interna)
                ↓
    ┌──────────────────────┐
    │   Auth Service       │ :8000
    │   Reservations       │ :8002
    │   Notifications      │ :5000
    │   Reports            │ :8001
    │   Audit              │ :5004
    └──────────────────────┘
```

### Flujo de Peticiones

1. Cliente envía petición al Gateway (puerto 3000)
2. Gateway valida autenticación (excepto rutas públicas)
3. Gateway añade headers internos (`X-API-Key`, `X-Gateway`)
4. Gateway reenvía petición al microservicio correspondiente
5. Gateway devuelve respuesta al cliente

## 📦 Requisitos

- Docker y Docker Compose
- Python 3.12+ (para desarrollo local)
- Acceso a red interna `app_net`

## 🔧 Instalación

### Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd api_gateway

# Construir la imagen
docker build -t api-gateway .

# Ejecutar con docker-compose desde el directorio raíz
cd ..
docker-compose up api-gateway
```

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python gateway.py
```

## ⚙️ Configuración

### Variables de Entorno

```env
# Servidor
PORT=3000
DEBUG=False

# Seguridad
API_KEY=xK7mP9nQ2wR5tY8uI1oL4jH6gS3aZ0bVcX8zL2kJ5hG

# URLs de Microservicios (red interna)
AUTH_SERVICE_URL=http://auth-service:8000
RESERVATION_SERVICE_URL=http://reservation-service:8002
NOTIFICATIONS_SERVICE_URL=http://notifications-service:5000
REPORTS_SERVICE_URL=http://reports-service:8001
AUDIT_SERVICE_URL=http://audit-service:5004
```

### Configuración en docker-compose.yml

```yaml
api-gateway:
  build:
    context: ./api_gateway
  ports:
    - "3000:3000"  # ÚNICO puerto público
  environment:
    API_KEY: "tu-api-key-segura"
    AUTH_SERVICE_URL: http://auth-service:8000
    # ... otros servicios
```

## 🚀 Uso

### Peticiones al Gateway

Todas las peticiones pasan por el puerto **3000**:

```bash
# Base URL
http://localhost:3000
```

### Autenticación

Rutas protegidas requieren token JWT en el header:

```bash
curl -X GET http://localhost:3000/api/reservas \
  -H "Authorization: Bearer <tu-token-jwt>"
```

### Rutas Públicas (sin autenticación)

- `/health` - Estado del gateway y servicios
- `/api/auth/login` - Inicio de sesión
- `/api/auth/register` - Registro de usuarios
- `/gateway/info` - Información del gateway

## 📡 Endpoints

### Gateway Endpoints

#### Health Check
```http
GET /health
```

**Respuesta:**
```json
{
  "success": true,
  "service": "api-gateway",
  "status": "healthy",
  "timestamp": "2024-01-20T10:30:00",
  "version": "1.0.0",
  "services": {
    "auth": {
      "status": "healthy",
      "url": "http://auth-service:8000",
      "response_time": 0.042
    },
    "reservations": { ... },
    "notifications": { ... },
    "reports": { ... },
    "audit": { ... }
  }
}
```
### Proxied Services

#### Autenticación
```http
POST /api/auth/login
POST /api/auth/register
GET  /api/auth/<path>
```

#### Reservas
```http
GET    /api/reservas
POST   /api/reservas
GET    /api/reservas/{id}
PUT    /api/reservas/{id}
DELETE /api/reservas/{id}
```
🔒 **Requiere autenticación**

#### Notificaciones
```http
GET    /api/notifications/<path>
POST   /api/notifications/<path>
PUT    /api/notifications/<path>
DELETE /api/notifications/<path>
```
🔒 **Requiere autenticación**

#### Reportes
```http
GET  /api/reports/<path>
POST /api/reports/<path>
```
🔒 **Requiere autenticación**

#### Auditoría
```http
GET  /api/audit/<path>
POST /api/audit/<path>
```
🔒 **Requiere autenticación**

## 🛠 Desarrollo

### Estructura del Proyecto

```
api_gateway/
├── Dockerfile           # Imagen Docker
├── gateway.py          # Código principal
├── requirements.txt    # Dependencias Python
└── README.md          # Este archivo
```
### Hacer Rutas Públicas

Añadir al array `PUBLIC_ROUTES`:

```python
PUBLIC_ROUTES = [
    '/api/auth/login',
    '/api/auth/register',
    '/tu/nueva/ruta/publica',
    '/health'
]
```

## 🐳 Despliegue

### Producción con Docker

```bash
# Construir
docker build -t api-gateway:latest .

# Ejecutar
docker run -d \
  -p 3000:3000 \
  --name api-gateway \
  --network app_net \
  -e API_KEY="tu-api-key-produccion" \
  api-gateway:latest
```

## 📊 Monitoreo

### Logs

Ver logs en tiempo real:

```bash
# Docker
docker logs -f api-gateway

# Docker Compose
docker-compose logs -f api-gateway
```

### Health Check

El contenedor tiene health check automático cada 30 segundos:

```bash
# Verificar estado
docker inspect api-gateway | grep -A 10 Health

# Manualmente
curl http://localhost:3000/health
```

### Métricas de Servicios

El endpoint `/health` proporciona:
- Estado de cada microservicio
- Tiempo de respuesta
- URL de conexión
- Errores de conectividad

## 🔒 Seguridad

### API Key

Todos los servicios internos validan la API Key:

```python
headers['X-API-Key'] = API_KEY
```

⚠️ **IMPORTANTE**: Cambiar la API Key en producción

### Headers de Seguridad

El gateway añade automáticamente:

- `X-Gateway`: Identifica peticiones del gateway
- `X-Forwarded-For`: IP del cliente original
- `X-API-Key`: Autenticación interna

### CORS

CORS está habilitado para todos los orígenes:

```python
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
```

## 🐛 Troubleshooting

### Error 503: Service Unavailable

- Verificar que el servicio destino esté corriendo
- Revisar conectividad en la red `app_net`
- Comprobar variables de entorno

```bash
docker-compose ps
docker network inspect app_net
```

### Error 504: Gateway Timeout

- Aumentar timeout en `proxy_request()` (default: 30s)
- Verificar rendimiento del servicio destino

### Error 401: No autorizado

- Verificar formato del token: `Bearer <token>`
- Comprobar que la ruta no esté en `PUBLIC_ROUTES`
- Validar token en el servicio de autenticación

## 📝 Ejemplos de Uso

### Login y Uso del Token

```bash
# 1. Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"123456"}'

# Respuesta: { "token": "eyJhbGc..." }

# 2. Usar token en peticiones
curl -X GET http://localhost:3000/api/reservas \
  -H "Authorization: Bearer eyJhbGc..."
```

### Crear Reserva

```bash
curl -X POST http://localhost:3000/api/reservas \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha": "2024-12-25",
    "hora": "14:00",
    "salon_id": 1,
    "num_personas": 4
  }'
```
---

## 🧾 Autor

- Autor: Manuela Zuluaga Cardona

---
