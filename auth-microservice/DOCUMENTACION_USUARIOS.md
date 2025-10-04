# 📚 Documentación del Auth Microservice - Gestión de Usuarios

## 🔐 Endpoints de Autenticación (Públicos)

### 1. Registrar Usuario
**POST** `/api/register`
```json
{
    "name": "Juan Pérez",
    "email": "juan@example.com", 
    "password": "password123",
    "password_confirmation": "password123",
    "role": "usuario"
}
```

### 2. Iniciar Sesión
**POST** `/api/login`
```json
{
    "email": "juan@example.com",
    "password": "password123"
}
```

### 3. Recuperar Contraseña
**POST** `/api/forgot-password`
```json
{
    "email": "juan@example.com"
}
```

### 4. Restablecer Contraseña
**POST** `/api/reset-password`
```json
{
    "token": "reset_token_here",
    "email": "juan@example.com",
    "password": "nueva_password123",
    "password_confirmation": "nueva_password123"
}
```

## 🔒 Endpoints Protegidos (Requieren token)

### 5. Cerrar Sesión
**POST** `/api/logout`
Headers: `Authorization: Bearer {token}`

### 6. Obtener Usuario Actual
**GET** `/api/me`
Headers: `Authorization: Bearer {token}`

## 👥 Gestión de Usuarios (Solo Administradores)

### 7. Listar Usuarios
**GET** `/api/usuarios?page=1&limit=10`
Headers: `Authorization: Bearer {admin_token}`

### 8. Obtener Usuario por ID
**GET** `/api/usuarios/{id}`
Headers: `Authorization: Bearer {admin_token}`

### 9. Actualizar Usuario
**PUT** `/api/usuarios/{id}`
Headers: `Authorization: Bearer {admin_token}`
```json
{
    "name": "Juan Carlos Pérez",
    "email": "juan.carlos@example.com",
    "role": "admin"
}
```

### 10. Eliminar Usuario
**DELETE** `/api/usuarios/{id}`
Headers: `Authorization: Bearer {admin_token}`

### 11. Buscar Usuarios
**POST** `/api/usuarios/buscar?page=1&limit=10`
Headers: `Authorization: Bearer {admin_token}`
```json
{
    "buscar": "juan"
}
```

### 12. Estadísticas de Usuarios
**GET** `/api/usuarios/stats`
Headers: `Authorization: Bearer {token}` (admin o usuario)

## 📋 Respuestas de Ejemplo

### Éxito (201/200)
```json
{
    "success": true,
    "message": "Usuario creado exitosamente",
    "data": {
        "usuario": {
            "id": 1,
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "role": "usuario",
            "created_at": "2025-09-29T10:00:00.000000Z"
        }
    }
}
```

### Error de Validación (422)
```json
{
    "success": false,
    "message": "Errores de validación",
    "errors": {
        "email": ["El email ya está registrado"]
    }
}
```

### Error de Autorización (403)
```json
{
    "success": false,
    "message": "Unauthorized. Required role: admin"
}
```

### Error de Autenticación (401)
```json
{
    "success": false,
    "message": "Unauthenticated"
}
```

## 🛡️ Roles y Permisos

### Administrador (`admin`)
- ✅ Acceso completo a gestión de usuarios
- ✅ Crear, leer, actualizar, eliminar usuarios
- ✅ Buscar usuarios y ver estadísticas

### Usuario Regular (`usuario`) 
- ✅ Solo puede ver estadísticas básicas
- ❌ No puede gestionar otros usuarios

## 🚀 Cómo Usar

1. **Registrarse como administrador:**
   ```bash
   curl -X POST http://localhost:8000/api/register \
   -H "Content-Type: application/json" \
   -d '{
     "name": "Admin",
     "email": "admin@example.com",
     "password": "admin123",
     "password_confirmation": "admin123", 
     "role": "admin"
   }'
   ```

2. **Iniciar sesión y obtener token:**
   ```bash
   curl -X POST http://localhost:8000/api/login \
   -H "Content-Type: application/json" \
   -d '{
     "email": "admin@example.com",
     "password": "admin123"
   }'
   ```

3. **Usar el token en las siguientes peticiones:**
   ```bash
   curl -X GET http://localhost:8000/api/usuarios \
   -H "Authorization: Bearer {tu_token_aqui}"
   ```

## 🔧 Instalación y Configuración

1. Instalar dependencias:
   ```bash
   composer install
   ```

2. Configurar base de datos en `.env`

3. Ejecutar migraciones:
   ```bash
   php artisan migrate
   ```

4. Iniciar servidor:
   ```bash
   php artisan serve
   ```

El microservicio estará disponible en: `http://localhost:8000`