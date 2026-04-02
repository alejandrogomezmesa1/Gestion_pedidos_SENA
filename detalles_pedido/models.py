from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from pedidos.models import Pedido
from productos.models import Producto

# Create your models here.

class DetallePedido(models.Model):
    detallesId = models.AutoField(primary_key=True)
    pedidoId = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    productoId = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "detalle_pedido"
        constraints = [
            models.UniqueConstraint(fields=['pedidoId', 'productoId'], name='unique_producto_por_pedido')
        ]

    def clean(self):
        if self.cantidad is None or self.cantidad < 1:
            raise ValidationError({'cantidad': 'La cantidad debe ser al menos 1.'})
        if self.productoId_id:
            producto = Producto.objects.get(pk=self.productoId_id)
            # Si es un detalle existente, recuperar la cantidad anterior para calcular diferencia
            cantidad_anterior = 0
            if self.pk:
                try:
                    cantidad_anterior = DetallePedido.objects.get(pk=self.pk).cantidad
                except DetallePedido.DoesNotExist:
                    cantidad_anterior = 0
            stock_disponible = producto.unidades_stock + cantidad_anterior
            if self.cantidad > stock_disponible:
                raise ValidationError(
                    {'cantidad': f'Stock insuficiente. Disponible: {stock_disponible} unidades.'}
                )

    def save(self, *args, **kwargs):
        producto = Producto.objects.get(pk=self.productoId_id)
        # Restaurar stock de cantidad anterior si es una actualización
        if self.pk:
            try:
                anterior = DetallePedido.objects.get(pk=self.pk)
                producto.unidades_stock += anterior.cantidad
            except DetallePedido.DoesNotExist:
                pass
        # Descontar nuevo stock
        producto.unidades_stock -= self.cantidad
        producto.save()
        # Calcular subtotal automáticamente
        self.subtotal = producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restaurar stock al eliminar el detalle
        producto = self.productoId
        producto.unidades_stock += self.cantidad
        producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Detalle del Pedido {self.pedidoId.pedidoId} - {self.productoId}"