# 🔐 Microservicio de Autenticación

Microservicio de seguridad y autenticación desarrollado con Laravel 8 y MySQL/MariaDB. Proporciona un sistema completo de autenticación con roles de usuario y endpoints RESTful para registro, login, logout y recuperación de contraseña.

## 🚀 Características

- ✅ **Autenticación con tokens** usando Laravel Sanctum
- ✅ **Sistema de roles básico** (admin/usuario)
- ✅ **Registro de usuarios** con validación
- ✅ **Login/Logout** funcional
- ✅ **Recuperación de contraseña** (estructura básica)
- ✅ **Middleware de roles** personalizado
- ✅ **Validación de datos** con Laravel Validator
- ✅ **Respuestas JSON** consistentes
- ✅ **Base para rate limiting** (Laravel por defecto)

## 🛠️ Tecnologías

- **Framework:** Laravel 8.x
- **Base de datos:** MySQL/MariaDB
- **Autenticación:** Laravel Sanctum
- **PHP:** ^7.3|^8.0
- **Validación:** Laravel Validation
- **Hashing:** Bcrypt

## 📋 Requisitos

- PHP >= 7.3
- Composer
- MySQL/MariaDB
- Extensiones PHP: OpenSSL, PDO, Mbstring, Tokenizer, XML, Ctype, JSON

## ⚡ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd auth-microservice
```

### 2. Instalar dependencias
```bash
composer install
```

### 3. Configurar ambiente
```bash
# Copiar archivo de configuración
cp .env.example .env

# Generar clave de aplicación
php artisan key:generate
```

### 4. Configurar base de datos
Editar el archivo `.env` con tus credenciales de base de datos:

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=auth_microservice
DB_USERNAME=tu_usuario
DB_PASSWORD=tu_contraseña
```

### 5. Ejecutar migraciones
```bash
php artisan migrate
```

### 6. Iniciar servidor
```bash
php artisan serve
```

El microservicio estará disponible en: `http://localhost:8000`

## 📚 API Endpoints

### 🔓 Endpoints Públicos

#### Registro de Usuario
```http
POST /api/register
Content-Type: application/json

{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "password": "password123",
    "password_confirmation": "password123",
    "role": "usuario" // opcional: "admin" o "usuario" (default: "usuario")
}
```

**Respuesta exitosa (201):**
```json
{
    "success": true,
    "message": "User registered successfully",
    "data": {
        "user": {
            "id": 1,
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "role": "usuario"
        },
        "token": "1|abc123...token"
    }
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
    "email": "juan@example.com",
    "password": "password123"
}
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "user": {
            "id": 1,
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "role": "usuario"
        },
        "token": "1|abc123...token"
    }
}
```

#### Recuperar Contraseña
```http
POST /api/forgot-password
Content-Type: application/json

{
    "email": "juan@example.com"
}
```

**Nota:** Requiere configuración de email en `.env` para funcionar completamente.

#### Resetear Contraseña
```http
POST /api/reset-password
Content-Type: application/json

{
    "token": "reset_token_from_email",
    "email": "juan@example.com",
    "password": "new_password123",
    "password_confirmation": "new_password123"
}
```

### 🔒 Endpoints Protegidos

> **Nota:** Todos los endpoints protegidos requieren el header de autorización:
> ```http
> Authorization: Bearer {tu_token}
> ```

#### Logout
```http
POST /api/logout
Authorization: Bearer {token}
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Logged out successfully"
}
```

#### Obtener Usuario Actual
```http
GET /api/me
Authorization: Bearer {token}
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "data": {
        "user": {
            "id": 1,
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "role": "usuario"
        }
    }
}
```

### 👨‍💼 Endpoints Solo para Admins

```http
GET /api/admin-example
Authorization: Bearer {admin_token}
```
*Nota: Actualmente no hay endpoints específicos implementados, pero la estructura está lista.*

### 👤 Endpoints Solo para Usuarios

```http
GET /api/user-example  
Authorization: Bearer {user_token}
```
*Nota: Actualmente no hay endpoints específicos implementados, pero la estructura está lista.*

## 🎭 Sistema de Roles

### Roles Disponibles

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| `admin` | Administrador del sistema | Acceso completo a todas las funcionalidades |
| `usuario` | Usuario regular | Acceso limitado a funcionalidades básicas |


## 📁 Estructura del Proyecto

```
auth-microservice/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   └── AuthController.php       # Controlador de autenticación
│   │   ├── Middleware/
│   │   │   └── RoleMiddleware.php       # Middleware de roles
│   │   └── Kernel.php                   # Registro de middleware
│   └── Models/
│       └── User.php                     # Modelo de usuario con roles
├── database/
│   └── migrations/
│       └── create_users_table.php       # Migración con campo role
├── routes/
│   └── api.php                          # Definición de rutas API
└── README.md
```

### Crear Usuario Administrador

```bash
php artisan tinker
```

```php
use App\Models\User;
use Illuminate\Support\Facades\Hash;

User::create([
    'name' => 'Administrador',
    'email' => 'admin@example.com',
    'password' => Hash::make('admin123'),
    'role' => 'admin'
]);
```

## 🚨 Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| `200` | Operación exitosa |
| `201` | Recurso creado exitosamente |
| `400` | Error en los datos enviados |
| `401` | No autenticado |
| `403` | Sin permisos (rol insuficiente) |
| `422` | Errores de validación |
| `500` | Error interno del servidor |

## 🔐 Seguridad

### Medidas Implementadas

- **Hashing de contraseñas** con Bcrypt
- **Tokens de acceso** con Laravel Sanctum
- **Validación básica** de inputs
- **Middleware de roles** personalizado
- **Estructura para rate limiting** (Laravel por defecto)
- **Protección básica** contra inyección SQL (Eloquent ORM)

## 🐛 Troubleshooting

### Problemas Comunes

**Error: "Key not found"**
```bash
php artisan key:generate
```

**Error de migración:**
```bash
php artisan migrate:fresh
```

**Token inválido:**
- Verificar que el token esté en el header correcto
- Verificar que el token no haya expirado

**Error 403 (Forbidden):**
- Verificar que el usuario tenga el rol correcto
- Verificar que el middleware esté registrado

---

## 🧾 Autor y repositorio

- Autor: Manuela Zuluaga Cardona
- Repositorio principal: https://github.com/mazuluagac/Proyecto_Sistema_de_Reservas.git

---
