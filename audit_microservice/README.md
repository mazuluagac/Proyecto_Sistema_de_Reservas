# 🕵️‍♂️ Microservicio de Auditoría

Microservicio en **Flask** para registrar y consultar eventos de auditoría en **MongoDB**. Diseñado para ser pequeño, fácil de probar e integrar en arquitecturas de microservicios.

---

## 📝 Descripción

Este microservicio expone endpoints REST simples para:

- Registrar eventos de auditoría (acción, usuario, timestamp, detalles).
- Consultar todos los eventos.
- Filtrar eventos por `action` y/o `user_id`.

Ideal para integrarse como componente de trazabilidad en sistemas distribuidos.

## 🛠️ Requisitos

| Requisito | Versión / nota |
|---|---|
| Python | 3.8+
| MongoDB | En ejecución (por defecto: `mongodb://localhost:27017`)
| Paquetes | `Flask`, `pymongo`

## 📦 Archivos principales

| Archivo | Descripción |
|---|---|
| `app.py` | Aplicación principal Flask con los endpoints de auditoría |

---

## ⚙️ Configuración

Por defecto la aplicación se conecta a MongoDB en mongodb://localhost:27017 y usa la base de datos microservicios y la colección audit_db. Si quieres cambiar esto puedes modificar directamente la cadena de conexión en app.py o mejorar la configuración usando variables de entorno (recomendado en producción).

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `MONGO_URI` | Cadena de conexión a MongoDB | `mongodb://localhost:27017`
| `PORT` | Puerto en el que corre la app | `5004`

## ▶️ Ejecutar

```powershell
python app.py
```

La aplicación corre por defecto en `http://localhost:5004` con `debug=True`.

## 📡 Endpoints

Resumen rápido en tabla:

| Método | Ruta | Descripción |
|---|---:|---|
| POST | `/audit` | Registra un evento. Body: `action`, `user_id`, `details` (opcional)
| GET | `/audit` | Lista todos los eventos
| GET | `/audit/buscar` | Filtra por `action` y/o `user_id` (query params)
| GET | `/` | Verifica que el servicio esté activo

Ejemplos:

Registrar evento:

```powershell
curl -X POST http://localhost:5004/audit -H "Content-Type: application/json" -d '{"action":"create_order","user_id":"u42","details":{"order_id":123}}'
```

Listar eventos:

```powershell
curl http://localhost:5004/audit
```

---

## 🗂️ Modelo de datos

Documento almacenado en la colección `audit_db`:

```json
{
   "action": "string",
   "user_id": "string|int",
   "fecha": "ISO8601 timestamp",
   "details": { }
}
```

## 🧪 Pruebas de Rendimiento con Locust

Este microservicio incluye una carpeta llamada `locust/` con un archivo de configuración (`locust_audit.py`) diseñado para ejecutar pruebas de rendimiento al microservicio de Auditoría.

Los resultados de las pruebas se han almacenado en la subcarpeta `locust/reports/`.

## ⚙️ Base de Datos para Pruebas

Para evitar sobrecargar o alterar los datos de producción, se ha creado una base de datos dedicada exclusivamente para pruebas de rendimiento:

- **Base de datos real:** audit_db

- **Base de datos de pruebas:** audit_db_test

🧩 Para utilizar la base de datos de pruebas, simplemente cambia el nombre en el archivo `app.py`:

```
auditoria_collection = db["audit_db_test"]
```
Esto permite realizar pruebas de carga de forma segura sin afectar los datos reales del sistema.
---

## 🧾 Autor y repositorio

- Autor: Manuela Zuluaga Cardona
- Repositorio principal: https://github.com/mazuluagac/Proyecto_Sistema_de_Reservas.git

---
