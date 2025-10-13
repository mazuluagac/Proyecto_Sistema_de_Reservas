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

Aplicar una arquitectura basada en **microservicios desacoplados**, que permita escalar, mantener y desplegar de manera independiente los módulos del sistema.

---

## 🧾 Autor

- Autor: Manuela Zuluaga Cardona

---
