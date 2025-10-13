from locust import HttpUser, task, between
import random
import json

class AuditoriaUser(HttpUser):
    # Espera entre 1 y 3 segundos entre tareas para simular usuarios reales
    wait_time = between(1, 3)

    @task(2)
    def crear_evento_auditoria(self):
        """Simula la creación de un evento (POST /audit)"""
        data = {
            "action": random.choice(["login", "logout", "create_user", "delete_user", "update_profile"]),
            "user_id": random.randint(1, 10),
            "details": {
                "ip": f"192.168.1.{random.randint(1, 255)}",
                "navegador": random.choice(["Chrome", "Firefox", "Edge"]),
            }
        }

        headers = {"Content-Type": "application/json"}
        with self.client.post("/audit", data=json.dumps(data), headers=headers, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Error al crear evento: {response.status_code}")

    @task(1)
    def obtener_eventos(self):
        """Simula consulta general de todos los eventos"""
        with self.client.get("/audit", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Error al obtener eventos: {response.status_code}")

    @task(1)
    def buscar_eventos_por_usuario(self):
        """Simula búsqueda filtrada de eventos"""
        user_id = random.randint(1, 10)
        action = random.choice(["login", "logout", "create_user", "delete_user"])
        params = {"user_id": user_id, "action": action}

        with self.client.get("/audit/buscar", params=params, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Error al buscar eventos: {response.status_code}")
