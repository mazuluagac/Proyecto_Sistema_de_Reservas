from rest_framework import serializers
from .models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Reserva con los campos:
    usuario_id, nombre_usuario, fecha_inicio, fecha_fin, descripcion, estado, created_at, updated_at
    """
    class Meta:
        model = Reserva
        fields = '__all__'
