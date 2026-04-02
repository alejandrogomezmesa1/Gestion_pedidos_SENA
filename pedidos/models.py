from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

class Pedido(models.Model):
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    TRANSICIONES_VALIDAS = {
        'pendiente':   ['procesando', 'cancelado'],
        'procesando':  ['enviado', 'cancelado'],
        'enviado':     ['entregado', 'cancelado'],
        'entregado':   [],
        'cancelado':   [],
    }

    pedidoId = models.AutoField(primary_key=True)
    clienteId = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='pendiente')

    class Meta:
        db_table = "pedido"

    def clean(self):
        if self.pk:
            estado_anterior = Pedido.objects.get(pk=self.pk).estado
            if estado_anterior != self.estado:
                permitidos = self.TRANSICIONES_VALIDAS.get(estado_anterior, [])
                if self.estado not in permitidos:
                    raise ValidationError(
                        {'estado': f'No se puede pasar de "{estado_anterior}" a "{self.estado}".'}
                    )

    def __str__(self):
        return f"Pedido de {self.clienteId} - {self.pedidoId}"

    
 
    

    
