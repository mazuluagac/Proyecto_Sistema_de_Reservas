# 🧩 Proyecto de Sistema de Reservas

Este proyecto implementa una arquitectura distribuida basada en **microservicios**, donde cada componente cumple una función independiente y se comunica mediante **APIs REST**.

---

## 🧠 Microservicios incluidos

| Microservicio | Descripción | Framework | Base de Datos |
|----------------|-------------|------------|----------------|
| **Auth + Usuarios** | Maneja la autenticación, registro y gestión de usuarios. | Laravel | MySQL |
| **Reservas** | Gestiona la creación, actualización y consulta de reservas. | Laravel | MySQL |
| **Reportes** | Genera reportes en PDF y Excel con datos de reservas simulados. | Django REST Framework | MySQL |
| **Notificaciones** | Envía notificaciones simuladas por correo o registra logs de notificación. | Flask | — |
| **Auditoría** | Registra acciones del sistema (logs de usuario, cambios, errores). | Flask | MongoDB |

---

## 🧰 Tecnologías principales

- **Laravel 8** — PHP framework para los servicios Auth y Reservas.  
- **Django REST Framework (DRF)** — API para la generación de reportes.  
- **Flask** — Microframework ligero para Notificaciones y Auditoría.  
- **MySQL** y **MongoDB** — Bases de datos relacional y NoSQL.  

---

## 🐳 Nueva integración con Docker Compose

Además de poder ejecutar cada microservicio de forma independiente, el proyecto ahora incluye un archivo docker-compose.yml que permite:

- Levantar todos los microservicios con un solo comando.

- Crear y vincular automáticamente las bases de datos necesarias.

- Ejecutar los servicios en su propio contenedor aislado.

- Simplificar el despliegue y las pruebas del sistema completo.

### ▶️ Ejecutar todo el ecosistema

Desde la raíz del proyecto:

```bash
docker-compose up 
```
Puedes detener todo el stack con:

```bash
docker-compose down 
```
### 🐳 Arquitectura Docker
```scss
┌──────────────────────┐
│    docker-compose     │
└───────────────────────┘
    │     │     │     │     │
    │     │     │     │     │
    ▼     ▼     ▼     ▼     ▼
 ┌─────────────┐ ┌──────────────┐ ┌───────────────┐ ┌──────────────┐ ┌──────────────┐
 │ Contenedor   │ │ Contenedor   │ │ Contenedor    │ │ Contenedor   │ │ Contenedor   │
 │ Laravel Auth │ │ Laravel Res. │ │ Django Reports│ │ Flask Notify │ │ Flask Audit  │
 └─────────────┘ └──────────────┘ └───────────────┘ └──────────────┘ └──────────────┘
      │                │               │                 │                 │
      ▼                ▼               ▼                 ▼                 ▼
  MySQL Auth       MySQL Res.      MySQL Reports     MySQL Auth / MySQL Res.        MongoDB
 (auth_db)         (reservation_db)   (reservation_db)     (auth_db / reservation_db )    (audit_db)
```
---

## ⚙️ Ejecución

Cada microservicio es **independiente**, por lo que debe ejecutarse en su propio entorno.

Ejemplo de puertos sugeridos:

| Servicio | Puerto |
|-----------|--------|
| Auth | 8000 |
| Reservas | 8002 |
| Reportes | 8001 |
| Notificaciones | 5000 |
| Auditoría | 5004 |

Ejecuta cada microservicio según las instrucciones específicas en su respectivo `README.md`.

---

## 🚀 Objetivo general

Construir un sistema basado en **microservicios desacoplados**, capaz de escalar y evolucionar por módulos, manteniendo independencia en despliegue, mantenimiento y pruebas.

---

## 🧾 Autor

- Autor: Manuela Zuluaga Cardona

---
