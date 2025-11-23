# 🧩 Proyecto de Sistema de Reservas

Este proyecto implementa una arquitectura distribuida basada en **microservicios**, donde cada componente cumple una función independiente y se comunica mediante **APIs REST**.

---

## 🧠 Microservicios incluidos

| Microservicio | Descripción | Framework | Base de Datos |
|----------------|-------------|------------|----------------|
| **API Gateway** | Punto central de entrada. Redirige solicitudes a los demás servicios. Maneja CORS, headers y seguridad. | Flask | — |
| **Auth + Usuarios** | Maneja la autenticación, registro y gestión de usuarios. | Laravel | MySQL |
| **Reservas** | Gestiona la creación, actualización y consulta de reservas. | Laravel | MySQL |
| **Reportes** | Genera reportes en PDF y Excel con datos de reservas simulados. | Django REST Framework | MySQL |
| **Notificaciones** | Envía notificaciones simuladas por correo o registra logs de notificación. | Flask | — |
| **Auditoría** | Registra acciones del sistema (logs de usuario, cambios, errores). | Flask | MongoDB |

---

## 🧰 Tecnologías principales

- **Laravel 8** — PHP framework para los servicios Auth y Reservas.  
- **Django REST Framework (DRF)** — API para la generación de reportes.  
- **Flask** — Microframework ligero para Notificaciones, Auditoría y API Gateway.  
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
┌──────────────────────────────┐
│         docker-compose       │
└──────────────────────────────┘
                │
                ▼
        ┌─────────────────┐
        │   API Gateway   │  ← ÚNICO expuesto al público (3000)
        └─────────────────┘
    ┌──────────┬──────────┬──────────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ Laravel │ │ Laravel │ │ Django       │ │ Flask       │ │ Flask Audit  │
│  Auth   │ │Reserva  │ │  Reports     │ │Notification │ │   Service    │
└─────────┘ └─────────┘ └──────────────┘ └─────────────┘ └──────────────┘
    │          │               │              │                │
    ▼          ▼               ▼              ▼                ▼
┌──────────┐ ┌────────────┐ ┌───────────┐ ┌──────────────────┐ ┌──────────┐
│ MySQL    │ │ MySQL      │ │ MySQL     │ │ MySQL auth /     │ │ MongoDB  │
│ auth_db  │ │ reserv_db  │ │ reserv_db │ │ MySQL reserv_db  │ │ audit_db │
└──────────┘ └────────────┘ └───────────┘ └──────────────────┘ └──────────┘

```
**Nota:** Para validar los nombres de los servicios acceda al docker-compose

---
## 🌉 API Gateway — Punto central de entrada al sistema

El proyecto ahora incluye un API Gateway desarrollado en Flask, el cual actúa como un único punto de entrada para todos los clientes externos.

Este Gateway cumple funciones clave:

## 🔐 1. Seguridad y validación unificada

- Inserta automáticamente un X-API-Key para comunicación interna.

- Normaliza Headers, tokens y autenticación.

- Previene exposición directa de los microservicios.

## 🔁 2. Enrutamiento inteligente

Redirige las peticiones hacia cada microservicio según la ruta:

| Ruta del Gateway | Redirige a |
|-----------|--------|
| /api/auth/... | Auth Service |
| /api/reservas/... | Reservation Service |
| /api/reports/... | Reports Service |
| /api/audit | Audit Service |

---
### 🏗️ Arquitectura Completa ( API Gateway incluido)

```txt
                          ┌───────────────────────┐
                          │      Frontend         │
                          │   (Vue / React)*      │
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌───────────────────────┐
                          │      API Gateway      │
                          │       (Flask)         │
                          └───────┬───────┬───────┘
             ┌────────────────────┘       │
             │                            │
             ▼                            ▼
  ┌───────────────────┐         ┌───────────────────┐
  │  Auth Service     │         │ Reservation Serv. │
  │    (Laravel)      │         │     (Laravel)     │
  └─────────┬─────────┘         └───────────┬───────┘
            │                               │
            ▼                               ▼
    ┌──────────────┐                ┌───────────────┐
    │  MySQL Auth  │                │ MySQL Reserv. │
    └──────────────┘                └───────────────┘
                                            │
                                            ▼
             ┌─────────────────────────────────────────┐
             │                                         │
             ▼                                         ▼
  ┌───────────────────┐                   ┌───────────────────┐
  │ Reports Service   │                   │ Notifications Serv│
  │   (Django DRF)    │                   │      (Flask)      │
  └──────────┬────────┘                   └───────────┬───────┘
             │                                        │
             ▼                                        ▼
    ┌───────────────┐                        ┌───────────────────┐
    │ MySQL Reserv. │                        │ MySQL Auth/ Reserv│
    └───────────────┘                        └───────────────────┘

                       ┌─────────────────────────────┐
                       │      Audit Service          │
                       │          (Flask)            │
                       └──────────────┬──────────────┘
                                      ▼
                               ┌──────────────┐
                               │   MongoDB    │
                               └──────────────┘

```
* (El frontend aún no está implementado, por lo que se deja como referencia en la arquitectura.)

## ⚙️ Ejecución

Cada microservicio es **independiente**, por lo que debe ejecutarse en su propio entorno.

Ejemplo de puertos sugeridos:

| Servicio | Puerto |
|-----------|--------|
| API Gateway | 3000 |
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
