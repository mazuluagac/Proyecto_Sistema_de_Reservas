 # 📊 Reports Microservice

Este microservicio provee un CRUD de reservas y generación de reportes en Excel y PDF.

## 📝 Descripción

Permite gestionar reservas (crear, listar, actualizar, eliminar) y descargar reportes de todas las reservas en formato Excel (.xlsx) y PDF (.pdf).

## 🛠️ Tecnologías utilizadas

- Python 3.10+
- Django 5.2.x
- Django REST Framework
- MySQL (según configuración en `settings.py`)
- `openpyxl` (para reportes Excel)
- `reportlab` (para reportes PDF)

## ⚙️ Ejecución local

1. Instala las dependencias mínimas:

```powershell
pip install django djangorestframework openpyxl reportlab mysqlclient
```

2. Configura la base de datos en `reports_microservice/reports_microservice/settings.py` según tu entorno.

3. Aplica migraciones:

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Inicia el servidor:

- Si ejecutas `python manage.py` sin argumentos, el proyecto iniciará por defecto en el puerto **8000** , 
para ejecutarlo en otro puerto, seguido de la instrucción `runserver` indica el puerto deseado (por ejemplo `python manage.py runserver 8001`).

```powershell
python manage.py
```

- Alternativamente, puedes indicar explícitamente el puerto (por ejemplo 8001):

```powershell
python manage.py runserver 8001
```

## 📦 Modelo: Reserva

| Campo   | Tipo      | Detalles |
|---------|-----------|----------|
| usuario | CharField | max_length=100 |
| estado  | CharField | choices: `pendiente`, `confirmada`, `cancelada` (default `pendiente`) |
| fecha   | DateField |  |

Archivo: `reports/models.py`

## 🚪 Endpoints implementados

| Ruta | Método | Descripción | Payload / Respuesta |
|------|--------|-------------|---------------------|
| `/api/reports/reservas/` | GET | Listar reservas | JSON list de reservas |
| `/api/reports/reservas/` | POST | Crear reserva | JSON: `{"usuario": "...", "estado": "...", "fecha": "YYYY-MM-DD"}` |
| `/api/reports/reservas/{id}/` | GET | Detalle de reserva | JSON con campos de la reserva |
| `/api/reports/reservas/{id}/` | PUT/PATCH | Actualizar reserva | JSON con campos a actualizar |
| `/api/reports/reservas/{id}/` | DELETE | Eliminar reserva | 204 No Content (esperado) |
| `/api/reports/excel/` | GET | Descargar reporte Excel (attachment) | Archivo `.xlsx` con columnas ID, Usuario, Estado, Fecha |
| `/api/reports/pdf/` | GET | Descargar reporte PDF (attachment) | Archivo `.pdf` con listado de reservas |

Archivos relevantes:
- `reports/serializers.py` (ReservaSerializer)
- `reports/views.py` (ReservaViewSet, ReporteExcelView, ReportePDFView)
- `reports/urls.py` (router y rutas de reportes)

---

## 🧾 Autor y repositorio

- Autor: Manuela Zuluaga Cardona
- Repositorio principal: https://github.com/mazuluagac/Proyecto_Sistema_de_Reservas.git

---
