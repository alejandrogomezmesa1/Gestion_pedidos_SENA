from rest_framework import serializers
from .models import DetallePedido

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'
