from locust import HttpUser, task, between

class NotificationUser(HttpUser):
    """
    Simula usuarios que acceden al microservicio de notificaciones
    para probar su rendimiento al enviar correos.
    """
    wait_time = between(1, 3)  # tiempo de espera entre solicitudes (en segundos)
    host = "http://localhost:5000"  # URL base del microservicio

    @task
    def send_notifications(self):
        """
        Endpoint que dispara el envío de notificaciones
        (se prueba sin pasar parámetros).
        """
        self.client.get("/send_reservation_notification")
