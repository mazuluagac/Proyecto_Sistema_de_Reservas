'''from locust import HttpUser, task, between

class ReportsUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8001"  # Cambia si tu microservicio corre en otra URL/puerto

    @task(1)
    def reporte_excel(self):
        self.client.get("/api/reports/excel/")

    @task(1)
    def reporte_pdf(self):
        self.client.get("/api/reports/pdf/")
'''

from locust import HttpUser, task, between

class ReportsUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8001"  # Cambia si tu microservicio corre en otra URL/puerto

    @task(1)
    def reporte_excel(self):
        # stream=True evita cargar todo el archivo en memoria
        with self.client.get("/api/reports/excel/", catch_response=True, stream=True) as response:
            if response.status_code != 200:
                response.failure(f"Fallo al generar Excel: {response.status_code}")
            else:
                response.success()

    @task(1)
    def reporte_pdf(self):
        with self.client.get("/api/reports/pdf/", catch_response=True, stream=True) as response:
            if response.status_code != 200:
                response.failure(f"Fallo al generar PDF: {response.status_code}")
            else:
                response.success()
