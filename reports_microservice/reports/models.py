from django.db import models


class Reserva(models.Model):
    usuario_id = models.IntegerField()
    nombre_usuario = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.CharField(max_length=255)
    estado = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'reservas'  # Usar la tabla existente
        managed = False        # No permitir que Django la gestione con migraciones

    def __str__(self):
        return f"{self.nombre_usuario} - {self.estado}"
