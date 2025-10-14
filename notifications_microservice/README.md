# 📧 Microservicio de Notificaciones

Microservicio desarrollado con Flask para enviar notificaciones por correo electrónico relacionadas con las reservas. Permite enviar correos automáticos según el estado de la reserva (confirmada, pendiente, cancelada, etc.) y consultar el email de un usuario específico.

## 🚀 Características

- ✅ **Envía notificaciones** por correo electrónico con HTML enriquecido
- ✅ **Diferenciación por estado:** confirmada, pendiente, cancelada, otros
- ✅ **Obtención de email de usuario** desde la base de datos de autenticación
- ✅ **Endpoints de prueba** para simular notificaciones
- ✅ **Configuración segura** usando variables de entorno
- ✅ **Compatible con pruebas de rendimiento** mediante Locust

## 🛠️ Tecnologías Utilizadas

- **Flask:** Microframework para Python utilizado para construir la API.
- **Flask-Mail:** Extensión de Flask para enviar correos electrónicos.
- **PyMySQL:** Conector de MySQL para Python, utilizado para interactuar con las bases de datos.
- **HTML/CSS:** Para la creación de correos electrónicos con formato enriquecido.
- **Locust:** Herramienta para pruebas de carga y rendimiento.

## 📋 Requisitos

- Python 3.6 o superior
- Flask
- Flask-Mail
- PyMySQL
- HTML/CSS
- Locust (opcional, para pruebas de rendimiento)

```bash
pip install flask flask-mail pymysql locust
```

## 🔧 Instalación

1. Clonar el repositorio
2. Crear un entorno virtual y activarlo
3. Instalar las dependencias    

```bash
pip install -r requirements.txt
```
## ⚙️ Configuración del correo electrónico

Editar los valores en el archivo principal `app.py` para configurar el servidor SMTP. Aquí hay un ejemplo de configuración para Gmail:

```bash
app.config['MAIL_USERNAME'] = 'tucorreo@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_password_de_aplicacion'
app.config['MAIL_DEFAULT_SENDER'] = 'tucorreo@gmail.com'
```

## 🏃‍♂️ Ejecución del Microservicio
Ejecutar el archivo `app.py`:

```bash
python app.py
```
El microservicio estará disponible en `http://localhost:5000`

## Configurar Bases de Datos
Configurar las conexiones a las bases de datos de autenticación y reservas en el archivo `app.py`:

- Base de datos de autenticación:
```python
auth_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_contraseña',
    'database': 'auth_db'
}
``` 

- Base de datos de reservas:
```python
reservations_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_contraseña',
    'database': 'reservations_db'
}
```

## 📦 Estructura del Proyecto

```
notification-microservice/
├── app.py                             # Código principal del microservicio
├── locust/
│   ├── locust_notification.py         # Archivo para pruebas de rendimiento con Locust
│   └── reports/                       # Carpeta donde se almacenan los reportes
├── README.md
└── requirements.txt              # Archivo de dependencias
```
## 🧪 Pruebas de Rendimiento con Locust
Para ejecutar pruebas de rendimiento, navega a la carpeta `locust` y ejecuta Locust:

```bash
locust -f locust_notifications.py
```
Luego, abre tu navegador y ve a `http://localhost:8089` para acceder a la interfaz de Locust.

- Los reportes se almacenan en:
```locust/reports/
```

## 📫 Endpoints Disponibles

**Enviar notificaciones de reserva**
```http
GET /send_reservation_notification
```

- Envia una notificación por correo electrónico basada en el estado de la reserva.

**Simular notificación de una reserva específica**
```http
GET /simulate_reservation_notification/{reservation_id}
```

- Simula el envío de una notificación por correo electrónico para una reserva específica.

**Usuarios** 
```http
GET /users/{user_id}
```

- Devuelve el email de un usuario según su ID.

## 🧾 Autor y repositorio
- Autor: Manuela Zuluaga Cardona
- Repositorio principal: https://github.com/mazuluagac/Proyecto_Sistema_de_Reservas.git

---