# Microservicio de Reservas 🏷️

Una microservicio de reservas ligero y probado, diseñado para gestionar la creación, consulta y administración de reservas de forma sencilla y escalable.

---

## ✨ Descripción general

Este microservicio expone una API REST para gestionar reservas (crear, listar, consultar, actualizar y eliminar). Está pensado para integrarse con otros servicios (autenticación, auditoría, notificaciones) dentro de una arquitectura de microservicios.

Principales características:

- Endpoints RESTful claros y documentados.
- Migraciones y seeders para datos iniciales.
- Configuración mediante variables de entorno.

---

## 🧰 Tecnologías utilizadas

- PHP (Laravel)
- Composer
- MySQL / MariaDB (u otra DB soportada por Laravel)

---

## 📋 Requisitos previos

- PHP >= 8.0 (ver composer.json para versión exacta)
- Composer
- MySQL o base de datos compatible
- Node.js & npm (solo si vas a compilar assets front-end)

---

## 🚀 Instalación y ejecución local

Sigue estos pasos en PowerShell (Windows) desde la raíz del proyecto:

```powershell
# 1. Instalar dependencias PHP
composer install

# 2. Copiar archivo de entorno y generar una clave
Copy-Item .env.example .env
php artisan key:generate

# 3. Configurar las variables de entorno en .env (ver sección "Configuración")

# 4. Ejecutar migraciones y seeders (si aplica)
php artisan migrate --seed

# 5. Ejecutar el servidor de desarrollo
php artisan serve --host=127.0.0.1 --port=8000

# Ahora la API estará disponible en: http://127.0.0.1:8000 (o el puerto configurado)
```
---

## 📡 Endpoints (API)

Nota: adapta los endpoints al prefijo real de `routes/api.php` si difiere.

| Método | Endpoint | Descripción |
|---|---:|---|
| GET | /api/reservas | Listar todas las reservas (paginado) |
| GET | /api/reservas/{id} | Obtener detalles de una reserva por ID |
| POST | /api/reservas | Crear una nueva reserva |
| PUT | /api/reservas/{id} | Actualizar una reserva existente |
| DELETE | /api/reservas/{id} | Eliminar una reserva |
| POST | /api/auth/login | (si aplica) Autenticar usuario / emitir token |

Ejemplo (crear reserva):

```json
POST /api/reservas
{
	"user_id": 1,
	"fecha": "2025-10-10",
	"hora_inicio": "14:00",
	"hora_fin": "16:00",
	"descripcion": "Reunión de proyecto"
}
```

Respuesta (ejemplo):

```json
{
	"id": 42,
	"user_id": 1,
	"fecha": "2025-10-10",
	"hora_inicio": "14:00",
	"hora_fin": "16:00",
	"descripcion": "Reunión de proyecto",
	"created_at": "2025-10-03T08:00:00Z"
}
```

---

## ⚙️ Configuración (variables de entorno)

Agrega estas variables en tu archivo `.env` (valores de ejemplo):

| Variable | Descripción | Ejemplo |
|---|---|---|
| APP_NAME | Nombre de la aplicación | "Reservation Service" |
| APP_ENV | Entorno | local |
| APP_KEY | Clave de la aplicación | base64:... |
| APP_DEBUG | Modo debug | true |
| APP_URL | URL base | http://127.0.0.1:8000 |
| DB_CONNECTION | Driver de BD | mysql |
| DB_HOST | Host de BD | 127.0.0.1 |
| DB_PORT | Puerto de BD | 3306 |
| DB_DATABASE | Nombre BD | reservations_db |
| DB_USERNAME | Usuario BD | root |
| DB_PASSWORD | Contraseña BD | secret |

Recuerda no commitear el `.env` con credenciales reales.

---

## 💡 Notas y recomendaciones

- Usa migraciones para mantener la consistencia del esquema.
- Añade validaciones y manejo de errores consistente en controladores.
- Agrega logging estructurado para facilitar debugging y monitoreo.
- Implementa autenticación (JWT / Passport / Sanctum) si la API va a ser pública.
- Considera agregar paginación y filtros en los endpoints de listado.

---

## 🧾 Autor y repositorio

- Autor: Manuela Zuluaga Cardona
- Repositorio principal: https://github.com/mazuluagac/Proyecto_Sistema_de_Reservas.git

---



