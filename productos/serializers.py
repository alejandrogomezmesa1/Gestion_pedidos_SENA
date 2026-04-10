from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    productoId = serializers.IntegerField(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'
