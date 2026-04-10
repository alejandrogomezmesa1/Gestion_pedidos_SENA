from django.core.exceptions import ValidationError
from django.db import models


class Pedido(models.Model):
    # Opciones válidas para el campo estado
    ESTADOS_CHOICES = [
        ('pendiente',  'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado',    'Enviado'),
        ('entregado',  'Entregado'),
        ('cancelado',  'Cancelado'),
    ]

    # Define los únicos cambios de estado permitidos.
    # Ejemplo: desde 'pendiente' solo se puede pasar a 'procesando' o 'cancelado'.
    # 'entregado' y 'cancelado' son estados finales: no admiten más transiciones.
    TRANSICIONES_VALIDAS = {
        'pendiente':   ['procesando', 'cancelado'],
        'procesando':  ['enviado',    'cancelado'],
        'enviado':     ['entregado',  'cancelado'],
        'entregado':   [],
        'cancelado':   [],
    }

    pedidoId     = models.AutoField(primary_key=True)
    # on_delete=CASCADE elimina los pedidos si se borra el cliente
    clienteId    = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)  # Se asigna automáticamente al crear
    estado       = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='pendiente')

    class Meta:
        db_table = "pedido"

    def clean(self):
        # Se ejecuta antes de guardar para validar reglas de negocio.
        # Solo valida si el pedido ya existe (pk distinto de None) y el estado cambió.
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

    
 
    

    
