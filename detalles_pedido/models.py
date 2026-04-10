from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from pedidos.models import Pedido
from productos.models import Producto


class DetallePedido(models.Model):
    detallesId = models.AutoField(primary_key=True)
    # FK al pedido: si se borra el pedido, se borran sus detalles (CASCADE)
    pedidoId   = models.ForeignKey(Pedido,   on_delete=models.CASCADE, related_name='detalles')
    # FK al producto: si se intenta borrar un producto con detalles, lanza error (PROTECT)
    productoId = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles')
    # MinValueValidator(1) impide guardar cantidad 0 o negativa
    cantidad   = models.IntegerField(validators=[MinValueValidator(1)])
    # El subtotal se calcula automáticamente en save(), no se ingresa manualmente
    subtotal   = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "detalle_pedido"
        # Se elimina la restricción de unicidad para permitir repeticiones
        # constraints = [
        #     models.UniqueConstraint(fields=['pedidoId', 'productoId'], name='unique_producto_por_pedido')
        # ]

    def clean(self):
        # Se llama antes de guardar para validar reglas de negocio.
        if self.cantidad is None or self.cantidad < 1:
            raise ValidationError({'cantidad': 'La cantidad debe ser al menos 1.'})
        if self.productoId_id:
            producto = Producto.objects.get(pk=self.productoId_id)
            # Si es una edición, se recupera la cantidad anterior para no penalizarla dos veces
            cantidad_anterior = 0
            if self.pk:
                try:
                    cantidad_anterior = DetallePedido.objects.get(pk=self.pk).cantidad
                except DetallePedido.DoesNotExist:
                    cantidad_anterior = 0
            # Stock real disponible = stock actual + lo que ya tenía reservado este detalle
            stock_disponible = producto.unidades_stock + cantidad_anterior
            if self.cantidad > stock_disponible:
                raise ValidationError(
                    {'cantidad': f'Stock insuficiente. Disponible: {stock_disponible} unidades.'}
                )

    def save(self, *args, **kwargs):
        producto = Producto.objects.get(pk=self.productoId_id)
        if self.pk:
            # Si es una actualización, primero se devuelve el stock que tenía antes
            try:
                anterior = DetallePedido.objects.get(pk=self.pk)
                producto.unidades_stock += anterior.cantidad
            except DetallePedido.DoesNotExist:
                pass
        # Se descuenta del stock la nueva cantidad
        producto.unidades_stock -= self.cantidad
        producto.save()
        # El subtotal se calcula automáticamente: precio × cantidad
        self.subtotal = producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Al eliminar un detalle, el stock del producto se restaura
        producto = self.productoId
        producto.unidades_stock += self.cantidad
        producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Detalle del Pedido {self.pedidoId.pedidoId} - {self.productoId}"