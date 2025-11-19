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

## 📁 Estructura del Proyecto

```
reservation-microservice/
├── app/
│   ├── Http/
│   │   ├── Controllers/                # Controlador de reservas
│   │   │   └── ReservaController.php
│   │   ├── Middleware/                 # Middlewares HTTP
│   │   └── Kernel.php                  # Registro de middleware
│   └── Models/
│       ├── Reserva.php                 # Modelo de reserva
│       └── User.php                    # Modelo de usuario
├── database/
│   ├── migrations/
│   │   ├── 2025_10_03_011917_create_reservas_table.php   # Migración reservas
│   │   └── ...                         # Otras migraciones
│   └── seeders/
│       └── DatabaseSeeder.php          # Seeder principal
├── routes/
│   ├── api.php                         # Definición de rutas API
├── locust/
│   ├── locust_reservation.py           # Archivo de pruebas de rendimiento con Locust
│   └── reports/                        # Carpeta donde se almacenan los reportes generados
└── README.md
```

---
---
## 🧪 Pruebas de Rendimiento con Locust

Este microservicio incluye una carpeta llamada `locust/` con un archivo de configuración (`locust_auth.py`) diseñado para ejecutar pruebas de rendimiento al microservicio de autenticación.

Los resultados de las pruebas se han almacenado en la subcarpeta `locust/reports/`.

## ⚙️ Base de Datos para Pruebas

Para evitar sobrecargar o alterar los datos de producción, se ha creado una base de datos dedicada exclusivamente para pruebas de rendimiento:

- **Base de datos real:** reservations_db

- **Base de datos de pruebas:** reservations_db_test

🧩 Para utilizar la base de datos de pruebas, simplemente cambia el nombre en el archivo `.env`:

```env
DB_DATABASE=reservations_db_test
```
Esto permite realizar pruebas de carga de forma segura sin afectar los datos reales del sistema.

### Para ejecutar las pruebas de rendimiento:
1. Asegúrate de tener Locust instalado. Si no lo tienes, puedes instalarlo usando pip:
   ```bash
   pip install locust
   ```  
2. Navega a la carpeta `locust/`:
   ```bash
   cd locust
   ```  
3. Ejecuta Locust especificando el archivo de pruebas:
   ```bash
   locust -f locust_reservation.py 
   ```
4. Abre tu navegador y ve a `http://localhost:8089` para acceder a la interfaz web de Locust.

---

## �📋 Requisitos previos

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

# 2. Configurar las variables de entorno en .env (ver sección "Configuración")

# 3. Ejecutar migraciones 
php artisan migrate --

# 4. Ejecutar el servidor de desarrollo
php artisan serve --host=127.0.0.1 --port=8002

# Ahora la API estará disponible en: http://127.0.0.1:8002 (o el puerto configurado)
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
  "usuario_id": 1,
  "nombre_usuario": "Pepito Perez",
  "fecha_inicio": "2025-11-20",
  "fecha_fin": "2025-11-20",
  "descripcion": "Reserva de sala de reuniones",
  "estado": "pendiente"
}
```

Respuesta (ejemplo):

```json
{
  "success": true,
  "message": "Reserva creada exitosamente",
  "data": {
    "usuario_id": 1,
    "nombre_usuario": "Pepito Perez",
    "fecha_inicio": "2025-11-20T00:00:00.000000Z",
    "fecha_fin": "2025-11-20T00:00:00.000000Z",
    "descripcion": "Reserva de sala de reuniones",
    "estado": "pendiente",
    "updated_at": "2025-11-19T06:54:32.000000Z",
    "created_at": "2025-11-19T06:54:32.000000Z",
    "id": 1
  }
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



