from locust import HttpUser, task, between
import random

class AuditUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:5004"

    @task(2)
    def crear_evento_simple(self):
        evento = {
            "action": random.choice(["login", "logout", "register", "update_profile"]),
            "user_id": f"user_{random.randint(1, 50)}",
            "details": {
                "status": random.choice(["success", "failed"])               
            }
        }
        self.client.post("/audit", json=evento)

    @task(1)
    def leer_eventos(self):
        self.client.get("/audit")