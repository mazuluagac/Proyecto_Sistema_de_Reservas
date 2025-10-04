from django.db import models

class Reserva(models.Model):
    usuario = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=20,
        choices=[("pendiente", "Pendiente"), ("confirmada", "Confirmada"), ("cancelada", "Cancelada")],
        default="pendiente"
    )
    fecha = models.DateField()

    def __str__(self):
        return f"{self.usuario} - {self.estado}"
