from locust import HttpUser, task, between
import random
import string

class AuthMicroserviceUser(HttpUser):
    wait_time = between(1, 3)  # tiempo entre tareas
    token = None

    def on_start(self):
        """Se ejecuta al inicio de cada usuario virtual."""
        # Opción 1: crear usuario nuevo
        name = ''.join(random.choices(string.ascii_letters, k=6))
        email = f"{name.lower()}@test.com"
        password = "password123"

        # Registro de usuario
        response = self.client.post("/api/register", json={
            "name": name,
            "email": email,
            "password": password,
            "password_confirmation": password,
            "role": "usuario"
        })

        if response.status_code == 201:
            print(f"Usuario {email} registrado con éxito.")
        else:
            print(f"Fallo al registrar usuario {email}: {response.text}")

        # Intentar login
        self.login(email, password)

    def login(self, email, password):
        """Login y almacenamiento del token de acceso."""
        response = self.client.post("/api/login", json={
            "email": email,
            "password": password
        })

        if response.status_code == 200:
            self.token = response.json()["data"]["token"]
            print("Login exitoso, token obtenido.")
        else:
            print("Error de login:", response.text)

    @task(3)
    def get_user_info(self):
        """Consultar datos del usuario autenticado."""
        if self.token:
            self.client.get(
                "/api/me",
                headers={"Authorization": f"Bearer {self.token}"}
            )

    """
    @task(2)
    def get_stats(self):
        #Consultar estadísticas de usuarios.
        if self.token:
            self.client.get(
                "/api/usuarios/stats",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    """

    @task(1)
    def logout(self):
        """Cerrar sesión del usuario."""
        if self.token:
            self.client.post(
                "/api/logout",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            self.token = None
