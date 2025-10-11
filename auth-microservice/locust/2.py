from locust import HttpUser, task, between
import random
import string

class AuthUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Se ejecuta cuando un usuario virtual inicia"""
        self.email = f"test{random.randint(1000, 9999)}@example.com"
        self.password = "password123"
        self.token = None
        self.register_user()
        self.login_user()
    
    def register_user(self):
        """Registrar un nuevo usuario"""
        payload = {
            "name": f"User{random.randint(1000, 9999)}",
            "email": self.email,
            "password": self.password,
            "password_confirmation": self.password,
            "role": "usuario"
        }
        
        self.client.post("/api/register", json=payload)
    
    def login_user(self):
        """Hacer login y guardar el token"""
        payload = {
            "email": self.email,
            "password": self.password
        }
        
        response = self.client.post("/api/login", json=payload)
        if response.status_code == 200:
            self.token = response.json()["data"]["token"]
    
    def get_headers(self):
        """Obtener headers con token de autenticación"""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    @task(3)
    def get_profile(self):
        """Obtener perfil del usuario (endpoint protegido)"""
        headers = self.get_headers()
        self.client.get("/api/me", headers=headers)
    
    @task(2)
    def list_users(self):
        """Listar usuarios (solo admin, pero lo intentamos)"""
        headers = self.get_headers()
        self.client.get("/api/usuarios", headers=headers)
    
    @task(2)
    def get_stats(self):
        """Obtener estadísticas"""
        headers = self.get_headers()
        self.client.get("/api/usuarios/stats", headers=headers)
    
    @task(1)
    def search_users(self):
        """Buscar usuarios"""
        headers = self.get_headers()
        payload = {"buscar": "test"}
        self.client.post("/api/usuarios/buscar", json=payload, headers=headers)
    
    @task(1)
    def logout(self):
        """Cerrar sesión"""
        headers = self.get_headers()
        self.client.post("/api/logout", headers=headers)
        # Después de logout, hacemos login again
        self.login_user()

class PublicUser(HttpUser):
    """Usuario que solo prueba endpoints públicos"""
    wait_time = between(2, 5)
    
    @task(3)
    def register(self):
        """Registrar usuario"""
        email = f"public{random.randint(10000, 99999)}@example.com"
        payload = {
            "name": f"PublicUser{random.randint(1000, 9999)}",
            "email": email,
            "password": "password123",
            "password_confirmation": "password123"
        }
        self.client.post("/api/register", json=payload)
    
    @task(5)
    def login(self):
        """Intentar login (usará credenciales por defecto)"""
        payload = {
            "email": "test@example.com",
            "password": "password123"
        }
        self.client.post("/api/login", json=payload)
    
    @task(2)
    def forgot_password(self):
        """Solicitar reset de contraseña"""
        payload = {
            "email": "test@example.com"
        }
        self.client.post("/api/forgot-password", json=payload)