from locust import HttpUser, task, between
import random
from datetime import datetime, timedelta

class ReservasUser(HttpUser):
    wait_time = between(3, 7)  # Simula pausas entre solicitudes
    host = "http://localhost:8002/api"  # Puerto configurado para el microservicio de reservas
    #iterations = 0
    #max_iterations = 4  # cada usuario hará 4 iteraciones

    # -----------------------------
    # 1️⃣ Crear una nueva reserva
    # -----------------------------
    # Lista de usuarios únicos para simular reservas más realistas
    usuarios = [
        {"usuario_id": i, "nombre_usuario": f"usuario_{i}"} for i in range(1, 20)
    ]

    @task(3)
    def crear_reserva(self):
        """Simula creación de una reserva con usuario consistente y menos repetitivo"""
        fecha_inicio = datetime.now().date()
        fecha_fin = fecha_inicio + timedelta(days=random.randint(1, 5))

        usuario = random.choice(self.usuarios)

        self.client.post("/reservas", json={
            "usuario_id": usuario["usuario_id"],
            "nombre_usuario": usuario["nombre_usuario"],
            "fecha_inicio": str(fecha_inicio),
            "fecha_fin": str(fecha_fin),
            "descripcion": random.choice(["Viaje de negocios", "Viaje familiar", "Descanso de fin de semana", "Evento especial"]),
            "estado": random.choice(["pendiente", "confirmada"])
        })

    # -----------------------------
    # 2️⃣ Obtener todas las reservas
    # -----------------------------
    @task(2)
    def listar_reservas(self):
        """Consulta todas las reservas"""
        self.client.get("/reservas")

    # -----------------------------
    # 3️⃣ Confirmar o cancelar reservas (aleatorio)
    # -----------------------------
    @task(1)
    def actualizar_estado(self):
        """Simula confirmación o cancelación de una reserva existente (si no hay, crea una primero)"""
        # Obtener la lista de reservas existentes
        response = self.client.get("/reservas")
        reservas = []
        if response.status_code == 200 and response.json():
            reservas = response.json()
            # Si la respuesta es paginada tipo Laravel, accede a 'data'
            if isinstance(reservas, dict) and 'data' in reservas:
                reservas = reservas['data']

        # Si no hay reservas, crear una antes de intentar actualizar
        if not reservas:
            self.crear_reserva()
            # Volver a consultar la lista de reservas
            response = self.client.get("/reservas")
            if response.status_code == 200 and response.json():
                reservas = response.json()
                if isinstance(reservas, dict) and 'data' in reservas:
                    reservas = reservas['data']

        if reservas:
            reserva = random.choice(reservas)
            reserva_id = reserva.get('id')
            accion = random.choice(["confirmar", "cancelar"])
            self.client.put(f"/reservas/{reserva_id}/{accion}")
