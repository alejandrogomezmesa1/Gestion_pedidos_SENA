from django.db import models

# Create your models here.

class Cliente(models.Model):
    clienteId = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    email = models.EmailField()
    dirección = models.CharField(max_length=100)
    teléfono = models.CharField(max_length=20)
    
    class Meta:
        db_table = "cliente"

    def __str__(self):
        return self.nombre_cliente     