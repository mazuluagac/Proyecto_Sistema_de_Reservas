 # 📊 Reports Microservice


Este microservicio está dedicado exclusivamente a la generación de reportes en Excel y PDF a partir de la tabla real `reservas` de la base de datos.

## 📝 Descripción

Permite descargar reportes de todas las reservas en formato Excel (.xlsx) y PDF (.pdf), con formato estético y todos los campos relevantes. No expone endpoints CRUD.

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

- Si ejecutas `python manage.py` sin argumentos, el proyecto iniciará por defecto en el puerto **8001**.

```powershell
python manage.py
```

- Alternativamente, puedes indicar explícitamente el puerto:

```powershell
python manage.py runserver 8001
```


## 📦 Modelo: Reserva

| Campo         | Tipo           | Detalles                                      |
|---------------|----------------|-----------------------------------------------|
| id            | AutoField      | Clave primaria (autoincremental)              |
| usuario_id    | IntegerField   | ID de usuario (relación o referencia externa) |
| nombre_usuario| CharField      | Nombre del usuario (max_length=100)           |
| fecha_inicio  | DateField      | Fecha de inicio de la reserva                 |
| fecha_fin     | DateField      | Fecha de fin de la reserva                    |
| descripcion   | CharField      | Descripción de la reserva (max_length=255)    |
| estado        | CharField      | `pendiente`, `confirmada`, `cancelada`        |
| created_at    | DateTimeField  | Fecha de creación (auto)                      |
| updated_at    | DateTimeField  | Fecha de actualización (auto)                 |

Archivo: `reports/models.py`


## 🚪 Endpoints implementados

| Ruta                   | Método | Descripción                          | Respuesta                  |
|------------------------|--------|--------------------------------------|----------------------------|
| `/api/reports/excel/`  | GET    | Descargar reporte Excel (attachment) | Archivo `.xlsx` con reservas (campos completos y formato estético)|
| `/api/reports/pdf/`    | GET    | Descargar reporte PDF (attachment)   | Archivo `.pdf` con reservas (campos completos y formato estético)|

Archivos relevantes:
- `reports/serializers.py` (ReservaSerializer)
- `reports/views.py` (ReporteExcelView, ReportePDFView)
- `reports/urls.py` (rutas de reportes)
---

## 🚦 Pruebas de rendimiento con Locust

1. Instala Locust:
```powershell
pip install locust
```

2. Ejecuta Locust desde la raíz del proyecto:
```powershell
locust -f locust/locust_reports.py
```

3. Abre tu navegador en [http://localhost:8089](http://localhost:8089) y configura los usuarios concurrentes para simular carga sobre los endpoints de reportes.

El archivo de pruebas ya está preparado para simular descargas concurrentes de Excel y PDF.

---

## 🧾 Autor y repositorio

- Autor: Manuela Zuluaga Cardona
- Repositorio principal: https://github.com/mazuluagac/Proyecto_Sistema_de_Reservas.git

---
