# Reports Microservice

Este microservicio provee un CRUD de reservas y generación de reportes en Excel y PDF.

## Descripción

Permite gestionar reservas (crear, listar, actualizar, eliminar) y descargar reportes de todas las reservas en formato Excel (.xlsx) y PDF (.pdf).

## Tecnologías utilizadas

- Python 3.10+
- Django 5.2.x
- Django REST Framework
- MySQL (según configuración en settings.py)
- openpyxl (para reportes Excel)
- reportlab (para reportes PDF)

## Ejecución local

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

```powershell
python manage.py runserver
```

## Endpoints implementados

- CRUD de reservas:
	- GET  `/api/reports/reservas/` → lista de reservas
	- POST `/api/reports/reservas/` → crear reserva
	- GET  `/api/reports/reservas/{id}/` → detalle
	- PUT/PATCH `/api/reports/reservas/{id}/` → actualizar
	- DELETE `/api/reports/reservas/{id}/` → eliminar

- Reportes:
	- GET `/api/reports/excel/` → descarga archivo Excel con todas las reservas
	- GET `/api/reports/pdf/` → descarga archivo PDF con todas las reservas

## Notas

- No hay autenticación ni permisos personalizados (AllowAny por defecto).
- Los reportes se generan en memoria y se envían como attachment.
- El archivo de tests existe pero no contiene pruebas implementadas.

---

Este README refleja únicamente lo que está implementado en el código del microservicio.
